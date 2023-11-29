#!/usr/bin/env python3
"""

Migration script to migrate CDS from 1.11.0 to 1.12.0
"""

import sys
from opensearchpy import Q
from maas_engine.update.migration import MaasMigrator, migration_main
from maas_cds.engines.reports.base import BaseProductConsolidatorEngine
from maas_cds.lib.parsing_name.parsing_name_s3 import extract_data_from_product_name_s3
from maas_cds.model import CdsDdpDataAvailable, CdsPublication, CdsProduct
from maas_cds.lib.dateutils import get_microseconds_delta

from maas_cds.update.task_monitoring import (
    TasksMonitoring,
    payload_to_tasks,
)


class PatchV1_12_0(MaasMigrator):
    """Migration tool to migrate from 1.11.0 to 1.12.0"""

    def __init__(self, args):
        super().__init__(args)

        self.tasks = TasksMonitoring()

    @payload_to_tasks(
        indexes=["cds-acquisition-pass-status", "raw-data-aps-product"],
        operation="delete_by_query",
    )
    def delete_aps_without_ground_station(self):
        dict_payload = {
            "query": {"query_string": {"query": "NOT ground_station: *"}},
        }

        return dict_payload

    @MaasMigrator.migration_action_iterator
    def update_transfer_time_compute_iterator(self):
        """This is not a task due to complexity of time management java vs python"""
        # approx 39056 document
        self.logger.info(
            "[update_transfer_time_compute] - START -%s documents impacted",
            CdsDdpDataAvailable.search().count(),
        )
        for document in (
            CdsDdpDataAvailable.search()
            .params(
                version=True,
                seq_no_primary_term=True,
            )
            .scan()
        ):
            document.transfer_time = get_microseconds_delta(
                document.time_start, document.time_finished
            )
            yield document.to_bulk_action()

        self.logger.info("[update_transfer_time_compute] - END ")

    @MaasMigrator.migration_action_iterator
    def s3_missing_field_iterator(self):
        """This is not a task due to complexity of string in tasks"""

        # PRODUCT

        query_product = (
            CdsProduct.search()
            .filter("term", mission="S3")
            .filter("bool", must_not=[Q("exists", field="timeliness")])
        )

        self.logger.info(
            "[s3_missing_field - product] - START - %s documents impacted",
            query_product.count(),
        )
        nb_product_updated = 0
        for document in query_product.params(
            version=True,
            seq_no_primary_term=True,
        ).scan():
            initial_dict = document.to_dict()

            data_dict = extract_data_from_product_name_s3(document.name)

            document.timeliness = data_dict.get(
                "timeliness", BaseProductConsolidatorEngine.TIMELINESS_NULL_VALUE
            )
            document.datatake_id = data_dict.get(
                "datatake_id",
            )

            if initial_dict | document.to_dict() != initial_dict:
                nb_product_updated += 1
                yield document.to_bulk_action()

        self.logger.info(
            "[s3_missing_field - product] - END - updated %s ",
            nb_product_updated,
        )

        # PUBLICATION

        query_publication = (
            CdsPublication.search()
            .filter("term", mission="S3")
            .filter("bool", must_not=[Q("exists", field="timeliness")])
        )

        self.logger.info(
            "[s3_missing_field - publication] - START - %s documents impacted",
            query_publication.count(),
        )
        nb_publication_updated = 0

        for document in query_publication.params(
            version=True,
            seq_no_primary_term=True,
        ).scan():
            initial_dict = document.to_dict()

            data_dict = extract_data_from_product_name_s3(document.name)

            document.timeliness = data_dict.get(
                "timeliness", BaseProductConsolidatorEngine.TIMELINESS_NULL_VALUE
            )
            document.datatake_id = data_dict.get(
                "datatake_id",
            )

            if initial_dict | document.to_dict() != initial_dict:
                nb_publication_updated += 1
                yield document.to_bulk_action()

        self.logger.info(
            "[s3_missing_field - publication] - END - updated %s ",
            nb_publication_updated,
        )

    def run(self):
        """override"""

        self.tasks.set_connection(self.es_conn)

        self.delete_aps_without_ground_station()
        self.bulk_exec(self.update_transfer_time_compute_iterator())
        self.bulk_exec(self.s3_missing_field_iterator())

        self.tasks.monitor(5)


def run():
    migration_main(sys.argv[1:], PatchV1_12_0)


if __name__ == "__main__":
    run()
