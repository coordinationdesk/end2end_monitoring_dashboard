#!/usr/bin/env python3
"""

Migration script to migrate CDS from 1.13.0 to 1.14.0
"""

import sys
import itertools
from maas_engine.update.migration import MaasMigrator, migration_main


from maas_cds.update.task_monitoring import (
    TasksMonitoring,
    payload_to_tasks,
)


class PatchV1_14_0(MaasMigrator):
    """Migration tool to migrate from 1.13.0 to 1.14.0"""

    def __init__(self, args):
        super().__init__(args)

        self.tasks = TasksMonitoring()

    @payload_to_tasks(
        indexes=["cds-product"],
        operation="update_by_query",
    )
    def update_dd_attribute_names(self):
        col_discriminator = [
            "deletion_cause",
            "deletion_date",
            "deletion_issue",
            "is_deleted",
        ]

        # itertools.product : produit cartésien
        patterns = [
            f"DD_{e[0]}_{e[1]}" for e in itertools.product("DHUS", col_discriminator)
        ]

        remove_scripts = ";".join([f"ctx._source.remove('{col}')" for col in patterns])

        script = (
            remove_scripts
            + ";"
            + "ctx._source.nb_dd_deleted = ctx._source.nb_dd_deleted - 4;"
        )

        dict_payload = {
            "query": {"query_string": {"query": "DD_D_deletion_cause: *"}},
            "script": {
                "source": script,
                "lang": "painless",
            },
        }

        yield dict_payload

    def run(self):
        """override"""

        self.tasks.set_connection(self.es_conn)

        self.update_dd_attribute_names()

        self.tasks.monitor(5)


def run():
    migration_main(sys.argv[1:], PatchV1_14_0)


if __name__ == "__main__":
    run()
