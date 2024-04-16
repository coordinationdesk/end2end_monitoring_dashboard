"""opensearch model classes for raw database"""
import datetime
import logging


from maas_model import datetime_to_zulu

from maas_collector.rawdata.meta import IngestionMeta


class ActionIterator:
    """Encapsulate Elastic search action building to feed bulk actions"""

    def __init__(
        self,
        path: str,
        config,
        force_update=False,
        chunk_size=1000,  # FIXME magic number
        report_name="",
        report_folder="",
        iter_callback=None,
    ):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.path = path

        self.config = config

        self.force_update = force_update

        self.chunk_size = chunk_size

        self.report_name = report_name

        self.report_folder = report_folder

        self.iter_callback = iter_callback

        self.action_iterator_errors = []

        # a map (indexname, identifier)=> callable for deferred execution of the #
        # iter_callback
        self.pending_callbacks = {}

        # store the identifier function as get_id_func() is a factory
        self.get_data_id = config.get_id_func()

        self.should_stop = False

        self.document_count = 0

        self.unmodified_ids = []

        self.has_partial = False

        # handle metadata
        self.meta = IngestionMeta(config, path)

        self.has_meta_file = self.meta.has_meta_file(path)

    def execute_callback(self, indexname: str, identifier: str):
        """Execute iteration callback.

        As iterator only produces data, properly calling the iterator_callback shall be
        done only after serialization is done and identifier is handled for messages.

        Args:
            indexname (str): index name
            identifier (str): document identifier
        """

        if not self.iter_callback:
            # nothing to do
            return

        key = (indexname, identifier)

        if key not in self.pending_callbacks:
            self.logger.warning("iter_callback not found for %s ", key)
            return

        try:
            self.pending_callbacks[key]()

        except Exception as error:
            self.logger.exception(error)
            self.logger.info("Ignoring call for %s", key)

        # free the callback
        del self.pending_callbacks[key]

    def stop(self):
        """Tell iterator and extractor to stop looping over extracted data"""
        self.logger.info("Action iterator should stop")
        self.should_stop = True
        self.config.extractor.stop()

    def process_document(self, document_id, data_extract, document) -> dict:
        """Insert, update or do nothing

        Args:
            document_id (str): document identifier
            data_extract (dict): extracted dictionnary
            document (Document): existing document or None for a new

        Returns:
            dict: bulk action ready dictionnary
        """
        if document is None:
            # new document
            document = self.config.model(**data_extract)

            document.meta.id = document_id

            document.ingestionTime = datetime.datetime.utcnow()

            # coerce fields : i.e. convert number strings to int, etc ...
            document.full_clean()

            document_dict = document.to_dict(include_meta=True)

            document_dict["_source"]["ingestionTime"] = datetime_to_zulu(
                datetime.datetime.utcnow()
            )

            document_dict["_index"] = document.partition_index_name
        else:
            # store existing dict for later comparison
            existing_dict = document.to_dict(include_meta=True)

            # set attributes to document instance
            for name, value in data_extract.items():
                setattr(document, name, value)

            # coerce fields : i.e. convert number strings to int,
            # date string to datetime objects, etc ...
            document.full_clean()

            document_dict = document.to_dict(include_meta=True)

            # test if document need update by merging existing with updated and
            # then compare with original.
            # this allows additionnal fields to exist in the index
            # remove reportName for comparison because of variable names of api payload
            source_compare_dict = document_dict["_source"].copy()

            del source_compare_dict["reportName"]

            if (
                existing_dict["_source"] | source_compare_dict
                == existing_dict["_source"]
            ):
                self.logger.debug("No need to update %s", document_id)

                self.unmodified_ids.append(document_id)

                if not self.force_update:
                    document_dict = None

            else:
                # update ingestionTime directly in the dict after comparison
                document_dict["_source"]["ingestionTime"] = datetime_to_zulu(
                    datetime.datetime.utcnow()
                )

        if self.iter_callback:
            self.pending_callbacks[
                (document.partition_index_name, document.meta.id)
            ] = lambda: self.iter_callback(document)

        return document_dict

    def process_chunk(self, data_chunk: list[dict]):
        """Ingest a list of extracted data

        Args:
            data_chunk (list[dict]): list of data extract

        Yields:
            [dict]: opensearch document
        """

        # list of identifiers for multiple get
        document_ids = [self.get_data_id(data_extract) for data_extract in data_chunk]

        for document_id, data_extract, document in zip(
            document_ids,
            data_chunk,
            self.config.model.mget_by_ids(document_ids, ignore_missing_index=True),
        ):
            try:
                document_dict = self.process_document(
                    document_id, data_extract, document
                )
            # catch broad exception to not break the ingestion for one bad record
            # pylint: disable=W0703
            except Exception as error:
                self.action_iterator_errors.append(
                    f"{self.path}: {str(error)} with {data_extract}"
                )
                if self.logger.getEffectiveLevel() == logging.DEBUG:
                    # for development
                    self.logger.error(
                        "%s: %s with %s", self.path, str(error), data_extract
                    )
                    self.logger.exception(error)
                    # FIXME store errors so collector can be error report
                else:
                    # for production
                    self.logger.warning("%s %s", self.path, str(error))
            else:
                if document_dict is not None:
                    if self.has_meta_file:
                        self.meta.populate(document_dict)

                    elif self.config.store_meta:
                        self.meta.update(document_dict)

                    self.document_count += 1

                    yield document_dict

    def __iter__(self):
        data_chunk = []

        for data_extract in self.config.extractor.extract(
            self.path, report_folder=self.report_folder
        ):
            if self.should_stop:
                break

            if self.report_name:
                self.logger.debug("Override reportName with '%s'", self.report_name)
                # override report name, useful for api as downloaded payload file is
                # the same at each query
                data_extract["reportName"] = self.report_name

            if self.report_folder:
                data_extract["reportFolder"] = self.report_folder

            # populate data chunk
            data_chunk.append(data_extract)

            if len(data_chunk) == self.chunk_size:
                # process chunk
                for document_dict in self.process_chunk(data_chunk):
                    if self.should_stop:
                        break

                    yield document_dict

                data_chunk.clear()

        if data_chunk:
            # flush remaining
            for document_dict in self.process_chunk(data_chunk):
                if self.should_stop:
                    break

                yield document_dict

        if self.config.store_meta and not self.has_meta_file:
            self.meta.dump(self.path)
