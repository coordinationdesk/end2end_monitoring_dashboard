#!/usr/bin/env python3
"""

Migration script to migrate CDS from 1.9.0 to 1.10.0
"""

import sys
from maas_engine.update.migration import MaasMigrator, migration_main

from maas_cds.update.task_monitoring import TasksMonitoring, payload_to_tasks


class PatchV1_10_0(MaasMigrator):
    """Migration tool to migrate from 1.8.0 to 1.9.0"""

    def __init__(self, args):
        super().__init__(args)

        self.tasks = TasksMonitoring()

    @payload_to_tasks(indexes=["cds-datatake"], operation="update_by_query")
    def remove_amalfi_completeness(self):

        dict_payload = {
            "script": {
                "source": 'ctx._source.remove("AMALFI_REPORT_local_value");ctx._source.remove("AMALFI_REPORT_local_expected");ctx._source.remove("AMALFI_REPORT_local_value_adjusted");ctx._source.remove("AMALFI_REPORT_local_percentage");ctx._source.remove("AMALFI_REPORT_local_status")',
                "lang": "painless",
            },
            "query": {"query_string": {"query": "AMALFI_REPORT_local_value: *"}},
        }

        return dict_payload

    @payload_to_tasks(indexes=["raw-data-mp-all-product"], operation="delete_by_query")
    def remove_mp_all_s2(self):
        dict_payload = {
            "query": {"query_string": {"query": "mission: S2"}},
        }

        return dict_payload

    @payload_to_tasks(indexes=["maas-collector-journal"], operation="update_by_query")
    def update_journal(self, interface_name, date):
        # date = 2021-12-15T08:30:00.549Z
        dict_payload = {
            "query": {"term": {"_id": interface_name}},
            "script": f'ctx._source.last_collect_date="{date}";ctx._source.last_date="{date}"',
        }

        return dict_payload

    @payload_to_tasks(indexes=["cds-s3-completeness"], operation="update_by_query")
    def update_s3_expected(self, product_type, expected):
        dict_payload = {
            "query": {
                "query_string": {
                    "query": f"product_type: {product_type} AND NOT expected: {expected}"
                }
            },
            "script": f"ctx._source.expected={expected}L;ctx._source.value_adjusted=Math.min(ctx._source.expected,ctx._source.value);ctx._source.percentage=ctx._source.value_adjusted/ctx._source.expected*100",
        }

        return dict_payload

    def run(self):
        """override"""

        self.tasks.set_connection(self.es_conn)

        self.remove_amalfi_completeness()

        self.remove_mp_all_s2()

        self.update_journal("S2MissionPlanningALL", "2022-03-01T00:00:00.000Z")

        self.tasks.monitor(5)

        self.update_s3_expected("DO_0_DOP___", 98 * 60 * 1000 * 1000)
        self.update_s3_expected("DO_0_NAV___", 98 * 60 * 1000 * 1000)
        self.update_s3_expected("GN_0_GNS___", 98 * 60 * 1000 * 1000)
        self.update_s3_expected("MW_0_MWR___", 98 * 60 * 1000 * 1000)

        self.update_s3_expected("SL_0_SLT___", 97 * 60 * 1000 * 1000)
        self.update_s3_expected("SL_1_RBT___", 97 * 60 * 1000 * 1000)
        self.update_s3_expected("SL_2_FRP___", 97 * 60 * 1000 * 1000)
        self.update_s3_expected("SL_2_LST___", 97 * 60 * 1000 * 1000)

        self.update_s3_expected("SR_0_SRA___", 92 * 60 * 1000 * 1000)
        self.update_s3_expected("SR_1_SRA___", 92 * 60 * 1000 * 1000)
        self.update_s3_expected("SR_1_SRA_A_", 92 * 60 * 1000 * 1000)
        self.update_s3_expected("SR_1_SRA_BS", 92 * 60 * 1000 * 1000)

        self.update_s3_expected("TM_0_HKM___", 98 * 60 * 1000 * 1000)
        self.update_s3_expected("TM_0_HKM2__", 98 * 60 * 1000 * 1000)
        self.update_s3_expected("MW_1_CAL___", 98 * 60 * 1000 * 1000)
        self.update_s3_expected("MW_1_MWR___", 98 * 60 * 1000 * 1000)

        self.tasks.monitor(5)


def run():
    migration_main(sys.argv[1:], PatchV1_10_0)


if __name__ == "__main__":
    run()
