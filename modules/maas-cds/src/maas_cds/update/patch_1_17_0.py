#!/usr/bin/env python3
"""

Migration script to migrate CDS from 1.16.0 to 1.17.0
"""

import sys
from maas_engine.update.migration import MaasMigrator, migration_main


from maas_cds.update.task_monitoring import (
    TasksMonitoring,
    payload_to_tasks,
)


class PatchV1_17_0(MaasMigrator):
    """Migration tool to migrate from 1.16.0 to 1.17.0"""

    def __init__(self, args):
        super().__init__(args)

        self.tasks = TasksMonitoring()

    @payload_to_tasks(
        indexes=["cds-product", "cds-publication", "cds-datatake-s1-s2"],
        operation="update_by_query",
    )
    def add_hex_datatake_id_to_datatake(self):
        dict_payload = {
            "query": {"query_string": {"query": "mission: S1 AND datatake_id: * AND NOT datatake_id: ______ AND NOT hex_datatake_id: * "}},
            "script": "int datatake_id_int=Integer.parseInt(ctx._source.datatake_id);String hex = Integer.toHexString(datatake_id_int);hex = hex.toUpperCase();ctx._source.hex_datatake_id=hex",
        }
        yield dict_payload

    @payload_to_tasks(
        indexes=["raw-data-interface-probe", "cds-interface-status"],
        operation="delete_by_query",
    )
    def remove_old_probe(self):
        
        interface_names = [
            'CADIP_Maspalomas_Files',
            'CADIP_Maspalomas_Qualityinfos',
            'metrics_LTA_Exprivia_S1',
            'metrics_LTA_Exprivia_S2',
            'metrics_LTA_Exprivia_S3',
            'CADIP_Svalbard_Files'
        ]

        for interface_name in interface_names:
            dict_payload = {
                "query": {"query_string": {"query": f"interface_name: {interface_name}"}}
            }
            yield dict_payload

    def run(self):
        """override"""

        self.tasks.set_connection(self.es_conn)

        self.add_hex_datatake_id_to_datatake()

        self.remove_old_probe()

        self.tasks.monitor(5)


def run():
    migration_main(sys.argv[1:], PatchV1_17_0)


if __name__ == "__main__":
    run()
