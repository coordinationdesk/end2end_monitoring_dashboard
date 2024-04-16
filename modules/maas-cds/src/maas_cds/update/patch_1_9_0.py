#!/usr/bin/env python3
"""

Migration script to migrate CDS from 1.8.0 to 1.9.0
"""

import sys
from maas_engine.update.migration import MaasMigrator, migration_main
from maas_cds.model import CdsDataflow, CdsPublication

from maas_cds.update.task_monitoring import TasksMonitoring


class PatchV1_9_0(MaasMigrator):
    """Migration tool to migrate from 1.8.0 to 1.9.0"""

    def __init__(self, args):
        super().__init__(args)

        self.tasks = TasksMonitoring()

    def SGS_MPS_switch(self):

        # payload for raw-data-aps-product
        dict_payload = {
            "script": {
                "source": "ctx._source.interface_name = 'DDP_MPS-Maspalomas'; ctx._source.production_service_name = 'MPS-Maspalomas'",
                "lang": "painless",
            },
            "query": {"query_string": {"query": "interface_name: DDP_SGS-Maspalomas"}},
        }

        self.logger.debug("[SGS_MPS_switch][raw-data-aps-product][START]")

        ubq = self.es_conn.update_by_query(
            index=["raw-data-aps-product"],
            body=dict_payload,
            params={
                "timeout": f"{self.args.es_timeout}s",
                "wait_for_completion": "false",
            },
        )
        self.tasks.append(
            {
                "id": ubq["task"],
                "name": "Ubq SGS_MPS_switch",
            }
        )
        self.logger.debug("[SGS_MPS_switch][raw-data-aps-product][END] %s", ubq)

    def remove_probe(self, interface_name):

        # payload for interface_name in raw-data-interface-probe-monitoring
        dict_payload = {"query": {"match": {"interface_name": interface_name}}}

        self.logger.debug(
            "[remove_probe_%s][raw-data-interface-probe-monitoring][INIT]",
            interface_name,
        )

        dbq = self.es_conn.delete_by_query(
            index=["raw-data-interface-probe-monitoring"],
            body=dict_payload,
            params={
                "timeout": f"{self.args.es_timeout}s",
                "wait_for_completion": "false",
            },
        )
        self.tasks.append(
            {
                "id": dbq["task"],
                "name": f"Dbq remove_probe in raw-data for {interface_name}",
            }
        )

        self.logger.debug(
            "[remove_probe_%s][raw-data-interface-probe-monitoring][STARTED] %s",
            interface_name,
            dbq,
        )

        self.logger.debug(
            "[remove_probe_%s][cds-interface-status-monitoring][INIT]", interface_name
        )

        dbq = self.es_conn.delete_by_query(
            index=["cds-interface-status-monitoring"],
            body=dict_payload,
            params={
                "timeout": f"{self.args.es_timeout}s",
                "wait_for_completion": "false",
            },
        )
        self.tasks.append(
            {
                "id": dbq["task"],
                "name": f"Dbq remove_probe in cds-interface for {interface_name}",
            }
        )

        self.logger.debug(
            "[remove_probe_%s][cds-interface-status-monitoring][STARTED] %s",
            interface_name,
            dbq,
        )

    def dataflow_search(self):
        """scan the index to retrieve all values

        Returns:
            scan result: scan result of the inex
        """
        search_request = CdsDataflow.search().query()
        scan_result = search_request.params(size=1000).execute()
        return scan_result

    def cds_publications_search(self, mission):
        """scan the index to retrieve all values

        Returns:
            scan result: scan result of the inex
        """
        search_request = CdsPublication.search().filter("term", mission=mission)

        search_request.aggs.metric(
            "product_type_aggs",
            "terms",
            field="product_type",
            size=1000,
        )

        res = search_request.execute()
        return res.aggregations.product_type_aggs["buckets"]

    def get_old_product_level(self, mission, product_type):
        search_request = (
            CdsPublication.search()
            .filter("term", mission=mission)
            .filter("term", product_type=product_type)
        ).params(size=1)

        res = list(search_request.execute())[0]
        product_dict = res.to_dict()

        try:
            return product_dict["product_level"]
        except KeyError:
            # self.logger.error(
            # "Unhandle case for %s - %s : %s", mission, product_type, product_dict
            # )
            return "___"

        # name = product_dict["name"]
        # data = extract_data_from_product_name(name)
        # return data["product_level"]

    def _get_migrations(self):

        search_result = self.dataflow_search()
        self.logger.info("[RUN] - START")

        dataflow_combinaisons = {
            f"{conf.mission}#{conf.product_type}": conf.level for conf in search_result
        }
        self.logger.info(
            "[RUN] - Find %s dataflow entities", len(dataflow_combinaisons)
        )

        migrations = {"OK": [], "KO": [], "TODO": [], "payload": []}
        publication_combinaisons_size = {}

        for mission in ["S1", "S2", "S3", "S5"]:
            publication_combinaisons = []
            self.logger.info("[RUN] - START - Mission: %s", mission)

            search_result = self.cds_publications_search(mission)
            publication_combinaisons = [
                f"{mission}#{item['key']}" for item in search_result
            ]

            for item in search_result:
                publication_combinaisons_size[f"{mission}#{item['key']}"] = item[
                    "doc_count"
                ]

            for combinaisons in publication_combinaisons:

                product_level = self.get_old_product_level(
                    combinaisons.split("#")[0], combinaisons.split("#")[1]
                )
                if combinaisons not in dataflow_combinaisons.keys():
                    migrations["KO"].append(combinaisons)
                    migrations["payload"].append(
                        (combinaisons.split("#")[0], combinaisons.split("#")[1], "___")
                    )
                    self.logger.debug("[MIGRATE][KO] - %s", combinaisons)

                elif dataflow_combinaisons[combinaisons] != product_level:
                    migrations["TODO"].append(combinaisons)
                    migrations["payload"].append(
                        (
                            combinaisons.split("#")[0],
                            combinaisons.split("#")[1],
                            dataflow_combinaisons[combinaisons],
                        )
                    )
                    self.logger.debug("[MIGRATE][TODO] - %s", combinaisons)

                else:
                    # preventive update
                    migrations["payload"].append(
                        (
                            combinaisons.split("#")[0],
                            combinaisons.split("#")[1],
                            dataflow_combinaisons[combinaisons],
                        )
                    )
                    migrations["OK"].append(combinaisons)
                    self.logger.debug("[MIGRATE][OK] - %s", combinaisons)

        nb_ok = len(migrations["OK"])
        impact_ok = sum(publication_combinaisons_size[k] for k in migrations["OK"])

        nb_todo = len(migrations["TODO"])
        impact_todo = sum(publication_combinaisons_size[k] for k in migrations["TODO"])

        nb_ko = len(migrations["KO"])
        impact_ko = sum(publication_combinaisons_size[k] for k in migrations["KO"])

        self.logger.info(
            "[STATS-APPROX] OK: (%s : %s) - TODO: (%s : %s) - KO :(%s : %s)",
            nb_ok,
            impact_ok,
            nb_todo,
            impact_todo,
            nb_ko,
            impact_ko,
        )

        return migrations

    def _generate_payload_migrations(self, migrations):
        for migration in migrations:

            (mission, product_type, new_product_level) = migration

            dict_payload = {
                "script": {
                    "source": f"ctx._source.product_level = '{new_product_level}'",
                    "lang": "painless",
                },
                "query": {
                    "query_string": {
                        "query": f"mission: {mission} AND product_type: {product_type} AND NOT product_level: {new_product_level}"
                    }
                },
            }

            yield [f"{mission} - {product_type} - {new_product_level}", dict_payload]

    def migrate_product_level(self, indexes):
        migrations = self._get_migrations()
        nb_migrations = len(migrations["payload"])
        nb_done = 0
        for [name, payload] in self._generate_payload_migrations(migrations["payload"]):

            payload_without_script = payload.copy()
            del payload_without_script["script"]

            count = self.es_conn.count(index=indexes, body=payload_without_script)

            if not self.args.dry_run:
                if count["count"]:
                    ubq = self.es_conn.update_by_query(
                        index=indexes,
                        body=payload,
                        params={
                            "timeout": f"{self.args.es_timeout}s",
                            "wait_for_completion": "false",
                        },
                    )
                    self.tasks.append(
                        {
                            "id": ubq["task"],
                            "name": f"Ubq product_level in {indexes} for {name}",
                        }
                    )
                    self.tasks.monitor(5)
                else:
                    self.logger.info(
                        "[COMPLETED] - Ubq product_level in %s for %s - 0 targeted",
                        indexes,
                        name,
                    )

                nb_done += 1
                self.logger.info(
                    "[PROGRESS][PRODUCT-LEVEL] - %s / %s - %s",
                    nb_done,
                    nb_migrations,
                    indexes,
                )
            else:
                self.logger.info("[DRY] - %s - Count: %s", name, count["count"])

    def migrate_montlhy_app_index(self):
        index_pattern = "raw-data-app-product"
        new_index_name = "raw-data-app-product-static"

        reindex_payload = {
            "source": {"index": "raw-data-app-product-2*"},
            "dest": {"index": f"{new_index_name}"},
        }

        result = self.es_conn.reindex(
            body=reindex_payload,
            timeout=f"{self.args.es_timeout}s",
            wait_for_completion=False,
        )

        self.logger.debug(result)

        index_list_to_delete = self.get_index_list(index_pattern)

        if new_index_name in index_list_to_delete:
            index_list_to_delete.remove(new_index_name)

        task = {
            "id": result["task"],
            "name": f"Reindexing {index_pattern} into {new_index_name}",
        }

        if index_list_to_delete:
            str_to_delete = ", ".join(index_list_to_delete)

            task["on_finish"] = (f"You can now delete  [ {str_to_delete} ]",)

        self.tasks.append(task)

    def migrate_forgot_oper(self):
        # payload for cds-product / publication
        dict_payload = {
            "script": {
                "source": "ctx._source.product_type = ctx._source.name.substring(9,19)",
                "lang": "painless",
            },
            "query": {"query_string": {"query": "mission: S1 AND product_type: OPER*"}},
        }

        self.logger.debug("[S1_product_type][START]")

        ubq = self.es_conn.update_by_query(
            index=["cds-product", "cds-publication"],
            body=dict_payload,
            params={
                "timeout": f"{self.args.es_timeout}s",
                "wait_for_completion": "false",
            },
        )
        self.tasks.append(
            {"id": ubq["task"], "name": "Ubq s1 product type cds-product_publication"}
        )

        self.logger.debug("[S1_product_type][END] %s", ubq)

    def remove_completeness_s5(self, product_types):
        indexes = "cds-s5-completeness"
        # payload for cds-s5-completeness
        dict_payload = {
            "query": {"bool": {"filter": {"terms": {"product_type": product_types}}}}
        }

        count = self.es_conn.count(index=indexes, body=dict_payload)
        count = count["count"]

        self.logger.debug(
            "[remove_completeness_s5][%s][INIT] %s entities", product_types, count
        )

        if not self.args.dry_run:

            dbq = self.es_conn.delete_by_query(
                index=["cds-s5-completeness"],
                body=dict_payload,
                params={
                    "timeout": f"{self.args.es_timeout}s",
                    "wait_for_completion": "false",
                },
            )
            self.tasks.append(
                {
                    "id": dbq["task"],
                    "name": f"Dbq cds-s5-completeness for {product_types}",
                }
            )

            self.logger.debug(
                "[remove_completeness_s5][%s][STARTED] %s",
                product_types,
                dbq,
            )
        else:
            self.logger.info(
                "[remove_completeness_s5][%s][DRY-RUN] would remove %s entities",
                product_types,
                count,
            )

    def run(self):
        """override"""

        self.tasks.set_connection(self.es_conn)

        self.SGS_MPS_switch()

        self.remove_probe("DD_ARCHIVE")
        self.remove_probe("DATAFLOW")

        self.migrate_montlhy_app_index()

        self.migrate_forgot_oper()

        self.remove_completeness_s5(
            ["OPER_L0__PDQ___", "OFFL_L1__CA_SIR", "OFFL_L1__CA_UVN"]
        )

        self.migrate_montlhy_app_index()

        self.migrate_forgot_oper()

        self.remove_completeness_s5(
            ["OPER_L0__PDQ___", "OFFL_L1__CA_SIR", "OFFL_L1__CA_UVN"]
        )

        self.migrate_montlhy_app_index()

        self.migrate_forgot_oper()

        self.remove_completeness_s5(
            ["OPER_L0__PDQ___", "OFFL_L1__CA_SIR", "OFFL_L1__CA_UVN"]
        )

        self.tasks.monitor()

        # this function is self monitored (to huge to delegate)
        self.migrate_product_level(
            indexes=[
                "cds-product-2022-11",
                "cds-product-2022-10",
                "cds-publication-2022-10",
                "cds-publication-2022-11",
            ]
        )

        self.tasks.finish()

        self.logger.info(
            "[READY] - First migration has ended you can start again collect"
        )

        self.migrate_product_level(indexes=["cds-product", "cds-publication"])


def run():
    migration_main(sys.argv[1:], PatchV1_9_0)


if __name__ == "__main__":
    run()
