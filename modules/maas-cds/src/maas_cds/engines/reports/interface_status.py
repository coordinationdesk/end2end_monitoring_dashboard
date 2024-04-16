"""Interface status consolidation"""
import datetime
import hashlib

from maas_engine.engine.rawdata import RawDataEngine

from maas_cds import model


class InterfaceStatusConsolidatorEngine(RawDataEngine):
    """Consolidate raw interface probes to interface status"""

    ENGINE_ID = "CONSOLIDATE_INTERFACE_STATUS"

    CONSOLIDATED_MODEL = model.CdsInterfaceStatus

    def __init__(
        self, args=None, send_reports=False, min_doi=None, refresh_interval_seconds=300
    ):
        super().__init__(args=args, send_reports=send_reports, min_doi=min_doi)

        self.refresh_delta = datetime.timedelta(seconds=refresh_interval_seconds)

    def consolidate_from_InterfaceProbe(
        self,
        raw_document: model.InterfaceProbe,
        documents: tuple[model.CdsInterfaceStatus],
    ) -> model.CdsInterfaceStatus:
        """
        Consolidated interface status from interface probe ingestion

        Args:
            raw_document (model.InterfaceProbe): raw document
            documents (tuple[model.CdsInterfaceStatus]): a pair of previous / next
                interface status. If status don't change, previous document will be
                extended. next is usually None except for replay / heavy load.

        Returns:
            model.CdsInterfaceStatus: CdsInterfaceStatus document
        """
        previous_document, next_document = documents

        if (
            previous_document
            and next_document
            and previous_document.status == next_document.status == raw_document.status
        ):
            # merge previous and next
            previous_document.status_time_stop = next_document.status_time_stop
            previous_document.calculate_duration()
            next_document.delete()
            return previous_document

        if previous_document:
            if previous_document.status == raw_document.status:
                # extend current status time range if previous probe is not too old
                previous_document.status_time_stop = raw_document.probe_time_stop

                # not need to create a new status document
                previous_document.calculate_duration()
                return previous_document

            if self.status_contains_probe(previous_document, raw_document):
                return self.split_status(previous_document, raw_document)

            # else
            previous_document.status_time_stop = raw_document.probe_time_start
            previous_document.calculate_duration()
            previous_document.save()

        if next_document:
            if next_document.status == raw_document.status:
                # extend current status time range if previous probe is not too old
                next_document.status_time_start = raw_document.probe_time_start

                # not need to create a new status document
                next_document.calculate_duration()
                return next_document

            # else
            next_document.status_time_start = raw_document.probe_time_stop
            next_document.calculate_duration()
            next_document.save()

        document = self.create_status_from_probe(raw_document)

        return document

    def status_contains_probe(
        self, status: model.CdsInterfaceStatus, probe: model.InterfaceProbe
    ) -> bool:
        """Check if a probe is contained in a status

        Args:
            status (model.CdsInterfaceStatus): status
            probe (model.InterfaceProbe): probe

        Returns:
            bool: True if probe is contained in the status
        """
        return (
            probe.probe_time_start >= status.status_time_start
            and probe.probe_time_stop <= status.status_time_stop
        )

    def split_status(
        self, status: model.CdsInterfaceStatus, probe: model.InterfaceProbe
    ) -> model.CdsInterfaceStatus:
        """Split a status and create a new one between the splitted parts

        Args:
            status (model.CdsInterfaceStatus): original status
            probe (model.InterfaceProbe): probe

        Returns:
            model.CdsInterfaceStatus: new status from the probe
        """

        new_status = self.create_status_from_probe(probe)

        new_status.status_time_stop = new_status.status_time_start + self.refresh_delta

        remaining_status = model.CdsInterfaceStatus()

        remaining_status.interface_name = status.interface_name

        remaining_status.status = status.status

        remaining_status.status_time_start = new_status.status_time_stop

        remaining_status.status_time_stop = status.status_time_stop

        status.status_time_stop = new_status.status_time_start
        status.calculate_duration()
        status.save()

        remaining_status.calculate_duration()
        remaining_status.updateTime = datetime.datetime.now(tz=datetime.timezone.utc)
        remaining_status.meta.id = self.generate_status_id(remaining_status)
        remaining_status.save()

        new_status.calculate_duration()

        return new_status

    def generate_status_id(self, status: model.CdsInterfaceStatus) -> str:
        """Generate a status identifier

        Args:
            status (model.CdsInterfaceStatus): status

        Returns:
            str: unique identifier
        """
        document_dict = status.to_dict()

        md5 = hashlib.md5()
        md5.update(status.interface_name.encode())
        md5.update(document_dict["status_time_start"].encode())
        md5.update(document_dict["status_time_stop"].encode())
        return md5.hexdigest()

    def create_status_from_probe(
        self, raw_document: model.InterfaceProbe
    ) -> model.CdsInterfaceStatus:
        """Factory function

        Args:
            raw_document (model.InterfaceProbe): probe

        Returns:
            model.CdsInterfaceStatus: status
        """

        # create a new status document
        document = model.CdsInterfaceStatus()

        document.interface_name = raw_document.interface_name

        document.status = raw_document.status

        # fill with probe data to have a non zero duration
        document.status_time_start = raw_document.probe_time_start

        document.status_time_stop = raw_document.probe_time_stop

        document.calculate_duration()

        document.meta.id = self.generate_status_id(document)

        return document

    def get_consolidated_documents(self) -> list[tuple[model.CdsInterfaceStatus]]:
        """

        Get or create the target documents for a one-to-one consolidation.
        """

        consolidated_documents = []

        for probe_document in self.input_documents:
            previous_status, next_status = None, None

            # find the previous status
            search = (
                model.CdsInterfaceStatus.search()
                .filter("term", interface_name=probe_document.interface_name)
                .filter(
                    "range", status_time_start={"lte": probe_document.probe_time_start}
                )
                .sort({"status_time_stop": {"order": "desc"}})
                .params(version=True, seq_no_primary_term=True, size=1, ignore=[404])
            )

            try:
                result = search.execute()

                if (
                    result
                    and (probe_document.probe_time_start - result[0].status_time_stop)
                    <= self.refresh_delta
                ):
                    previous_status = result[0]
                    self.logger.debug("Found previous status: %s", previous_status)

            except KeyError:
                previous_status = None

            # try find the next status. this is not the nominal case but it may happen
            search = (
                model.CdsInterfaceStatus.search()
                .filter("term", interface_name=probe_document.interface_name)
                .filter(
                    "range", status_time_start={"gt": probe_document.probe_time_stop}
                )
                .sort({"status_time_start": {"order": "asc"}})
                .params(version=True, seq_no_primary_term=True, size=1, ignore=[404])
            )

            try:
                result = search.execute()

                if (
                    result
                    and (result[0].status_time_start - probe_document.probe_time_stop)
                    <= self.refresh_delta
                ):
                    next_status = result[0]
                    self.logger.debug("Found next status: %s", next_status)

            except KeyError:
                previous_status = None

            consolidated_documents.append((previous_status, next_status))

        return consolidated_documents
