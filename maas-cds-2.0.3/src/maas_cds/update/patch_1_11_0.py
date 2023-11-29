#!/usr/bin/env python3
"""

Migration script to migrate CDS from 1.10.0 to 1.11.0
"""

import sys
from maas_engine.update.migration import MaasMigrator, migration_main
from maas_cds.model.cds_s5_completeness import CdsS5Completeness

from maas_cds.update.task_monitoring import (
    TasksMonitoring,
    payload_to_tasks,
)


class PatchV1_11_0(MaasMigrator):
    """Migration tool to migrate from 1.10.0 to 1.11.0"""

    def __init__(self, args):
        super().__init__(args)

        self.tasks = TasksMonitoring()

    @payload_to_tasks(indexes=["cds-s5-completeness"], operation="update_by_query")
    def update_expected_s5_completeness(self):

        # no need dataflow it's why i allow myself
        for product_type, value in CdsS5Completeness._BASE_S5_PRODUCTS_TYPES.items():
            expected = value["sensing"]
            dict_payload = {
                "query": {
                    "query_string": {
                        "query": f"product_type: {product_type} AND NOT expected: {expected}"
                    }
                },
                "script": f"ctx._source.expected={expected}L;ctx._source.value_adjusted=Math.min(ctx._source.expected,ctx._source.value);ctx._source.percentage=ctx._source.value_adjusted/ctx._source.expected*100;if (ctx._source.percentage >= 100){{ctx._source.status = 'Complete'}} else if (ctx._source.percentage > 0) {{ctx._source.status = 'Partial'}} else {{ctx._source.status = 'Missing'}}",
            }

            yield dict_payload

    def run(self):
        """override"""

        self.tasks.set_connection(self.es_conn)

        self.update_expected_s5_completeness()

        self.tasks.monitor(5)


def run():
    migration_main(sys.argv[1:], PatchV1_11_0)


if __name__ == "__main__":
    run()
