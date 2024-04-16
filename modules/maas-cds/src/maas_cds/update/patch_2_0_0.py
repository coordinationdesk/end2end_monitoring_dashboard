#!/usr/bin/env python3
"""

Migration script to migrate CDS from 1.19.0 to 2.0.0
"""

import sys
from maas_engine.update.migration import MaasMigrator, migration_main


from maas_cds.update.task_monitoring import (
    TasksMonitoring,
    payload_to_tasks,
)


class PatchV2_0_0(MaasMigrator):
    """Migration tool to migrate from 1.19.0 to 2.0.0"""

    def __init__(self, args):
        super().__init__(args)

        self.tasks = TasksMonitoring()

    @payload_to_tasks(
        indexes=["cds-edrs-acquisition-pass-status", "raw-data-aps-edrs"],
        operation="delete_by_query",
    )
    def delete_all_edrs_aps(self):
        dict_payload = {
            "query": {"query_string": {"query": "*"}},
        }
        yield dict_payload

    @payload_to_tasks(
        indexes=["cds-acquisition-pass-status"],
        operation="update_by_query",
    )
    def add_from_acq_timeliness_ddp(self):
        dict_payload = {
            "query": {
                "query_string": {"query": "first_frame_start:* AND stop_delivery:*"}
            },
            "script": "ctx._source.from_acq_delivery_timeliness = ChronoUnit.MICROS.between(ZonedDateTime.parse(ctx._source.first_frame_start), ZonedDateTime.parse(ctx._source.stop_delivery))",
        }
        yield dict_payload

    @payload_to_tasks(
        indexes=["cds-cadip-acquisition-pass-status"],
        operation="update_by_query",
    )
    def add_from_acq_timeliness_cadip(self):
        dict_payload = {
            "query": {
                "query_string": {"query": "downlink_start:* AND delivery_stop:*"}
            },
            "script": "ctx._source.from_acq_delivery_timeliness = ChronoUnit.MICROS.between(ZonedDateTime.parse(ctx._source.downlink_start), ZonedDateTime.parse(ctx._source.delivery_stop))",
        }
        yield dict_payload

    @payload_to_tasks(
        indexes=["raw-data-aps-product"],
        operation="update_by_query",
    )
    def update_aps_raw_data_daily_field(self):
        dict_payload = {
            "query": {"query_string": {"query": "NOT report_type:*"}},
            "script": "ctx._source.report_type = 'daily'",
        }
        yield dict_payload

    @payload_to_tasks(
        indexes=["cds-product", "cds-publication"],
        operation="delete_by_query",
    )
    def delete_product_level_A(self):
        dict_payload = {
            "query": {"query_string": {"query": "product_type : S1*ETA__AX*"}},
        }

        return dict_payload

    def run(self):
        """override"""

        self.tasks.set_connection(self.es_conn)

        self.add_from_acq_timeliness_ddp()
        self.add_from_acq_timeliness_cadip()
        self.update_aps_raw_data_daily_field()
        self.delete_all_edrs_aps()

        self.delete_product_level_A()

        self.tasks.monitor(5)


def run():
    migration_main(sys.argv[1:], PatchV2_0_0)


if __name__ == "__main__":
    run()
