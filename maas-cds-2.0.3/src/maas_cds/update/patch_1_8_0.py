#!/usr/bin/env python3
"""

Migration script to migrate CDS from 1.7.0 to 1.8.0
"""
import sys
from maas_engine.update.migration import MaasMigrator, migration_main

from maas_cds.update.task_monitoring import TasksMonitoring


class PatchV1_8_0(MaasMigrator):
    """Migration tool to migrate from 1.7.0 to 1.8.0"""

    def __init__(self, args):
        super().__init__(args)

        self.tasks = TasksMonitoring()

    def reindexes_operation(self):
        reindex_list = [
            {"index_name": "cds-datatake", "new_index_name": "cds-datatake-s1-s2"},
            {"index_name": "cds-ddp-data-available"},
            {"index_name": "cds-downlink-datatake"},
            {"index_name": "cds-s3-completeness"},
            {"index_name": "cds-s5-completeness"},
            {"index_name": "cds-sat-unavailability"},
            {"index_name": "raw-data-app-product"},
            {"index_name": "raw-data-aps-product"},
            {"index_name": "raw-data-auxip-product"},
            {"index_name": "raw-data-cams-tickets"},
            {
                "index_name": "raw-data-dd-product",
                "new_index_name": "raw-data-dd-product-2022",
            },
            {"index_name": "raw-data-ddp-data-available"},
            {"index_name": "raw-data-mp-all-product"},
            {"index_name": "raw-data-mp-product"},
            {"index_name": "raw-data-sat-unavailability-product"},
        ]

        for start_index in ["1", "2"]:
            for reindex in reindex_list:
                index_pattern = f"{reindex['index_name']}-{start_index}*"
                new_index_name = (
                    f"{reindex['index_name']}-static"
                    if "new_index_name" not in reindex
                    else reindex["new_index_name"]
                )

                # install new template
                self.install_index(reindex["index_name"])

                reindex_payload = {
                    "source": {"index": index_pattern},
                    "dest": {"index": new_index_name},
                }

                result = self.es_conn.reindex(
                    body=reindex_payload,
                    timeout=f"{self.args.es_timeout}s",
                    wait_for_completion=False,
                )

                self.logger.debug(result)

                self.logger.debug(
                    "Wait all data is in %s index now you can delete previous index",
                    new_index_name,
                )

                index_list_to_delete = self.get_index_list(reindex["index_name"])

                if new_index_name in index_list_to_delete:
                    index_list_to_delete.remove(new_index_name)

                task = {
                    "id": result["task"],
                    "name": f"Reindexing {reindex['index_name']} {start_index}",
                }
                if index_list_to_delete:
                    str_to_delete = ", ".join(index_list_to_delete)

                    task["on_finish"] = (f"You can now delete  [ {str_to_delete} ]",)

                self.tasks.append(task)

    def fix_s5p_product_level(self):

        # payload for cds-s5-completeness
        dict_payload = {
            "script": {
                "source": "ctx._source.product_level = 'L1B'",
                "lang": "painless",
            },
            "query": {
                "query_string": {
                    "query": "product_level: L1_ AND product_type: *_L1B_*"
                }
            },
        }

        # s5-completeness
        self.logger.debug("[S5P_product_level][cds-s5-completeness][START]")
        ubq = self.es_conn.update_by_query(
            index=["cds-s5-completeness"],
            body=dict_payload,
            params={
                "timeout": f"{self.args.es_timeout}s",
                "wait_for_completion": "false",
            },
        )
        self.tasks.append(
            {"id": ubq["task"], "name": "Ubq s5 product level cds-s5-completeness"}
        )
        self.logger.debug("[S5P_product_level][cds-s5-completeness][END] %s", ubq)

        # payload for cds-product and cds-publication
        dict_payload = {
            "script": {
                "source": "ctx._source.product_level = 'L1B'",
                "lang": "painless",
            },
            "query": {
                "query_string": {
                    "query": "product_level: L1_ AND name: *_L1B_* AND mission: S5"
                }
            },
        }

        # product and publication
        self.logger.debug("[S5P_product_level][cds-product,cds-publication][START]")
        ubq = self.es_conn.update_by_query(
            index=["cds-product", "cds-publication"],
            body=dict_payload,
            params={
                "timeout": f"{self.args.es_timeout}s",
                "wait_for_completion": "false",
            },
        )
        self.tasks.append(
            {
                "id": ubq["task"],
                "name": "Ubq s5 product level cds-product/cds-publication",
            }
        )
        self.logger.debug(
            "[S5P_product_level][cds-product,cds-publication][END] %s",
            ubq,
        )

    def product_enrichment(self):

        # payload for cds-product
        dict_payload = {
            "script": {
                "source": "ctx._source.from_prip_ddip_timeliness = ChronoUnit.MICROS.between(ZonedDateTime.parse(ctx._source.prip_publication_date),ZonedDateTime.parse(ctx._source.ddip_publication_date))",
                "lang": "painless",
            },
            "query": {
                "query_string": {
                    "query": "prip_publication_date:* AND ddip_publication_date:* AND NOT from_prip_ddip_timeliness: *"
                }
            },
        }

        self.logger.debug("[product_enrichment][cds-product][START]")

        ubq = self.es_conn.update_by_query(
            index=["cds-product"],
            body=dict_payload,
            params={
                "timeout": f"{self.args.es_timeout}s",
                "wait_for_completion": "false",
            },
        )
        self.tasks.append(
            {
                "id": ubq["task"],
                "name": "Ubq ddip_timeliness cds-product",
            }
        )
        self.logger.debug("[product_enrichment][cds-product][END] %s", ubq)

    def run(self):
        """override"""

        self.tasks.set_connection(self.es_conn)

        self.reindexes_operation()

        self.tasks.monitor()

        self.fix_s5p_product_level()

        self.tasks.monitor()

        self.product_enrichment()

        self.tasks.monitor()

        self.tasks.finish()


def run():
    migration_main(sys.argv[1:], PatchV1_8_0)


if __name__ == "__main__":
    run()
