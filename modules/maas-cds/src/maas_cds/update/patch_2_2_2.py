#!/usr/bin/env python3
"""

Migration script to migrate CDS from 2.2.0 to 2.2.2
"""

import sys
from maas_engine.update.migration import MaasMigrator, migration_main


from maas_cds.update.task_monitoring import (
    TasksMonitoring,
    payload_to_tasks,
)


class PatchV2_2_2(MaasMigrator):
    """Migration tool to migrate from 2.2.0 to 2.2.2"""

    def __init__(self, args):
        super().__init__(args)

        self.tasks = TasksMonitoring()

    @payload_to_tasks(
        indexes=["cds-cams-tickets"],
        operation="update_by_query",
    )
    def migrate_cams_index(self):
        dict_payload = {
            "query": {"query_string": {"query": "key: *"}},
            "script": """
            // Replace old urls with new url
            def url = ctx._source.url;
            if (url != null) {
                url = url.substring(30); // Remove old url
                url = "https://esa-cams.atlassian.net/browse/" + url; // add new url
                ctx._source.url = url;
                }

            // Process 'key' attribute (PDGSANOM to GSANOM)
            def key = ctx._source.key;
            if (key != null && key.length() > 2) {
                key = key.substring(2); // Remove the first 2 characters
                ctx._source.key = key;
            }
            """,
        }
        yield dict_payload

    @payload_to_tasks(
        indexes=[
            "cds-s3-completeness",
            "cds-s5-completeness",
            "cds-cadip-acquisition-pass-status",
            "cds-edrs-acquisition-pass-status-product",
            "cds-hktm-acquisition-completeness",
            "cds-product",
            "cds-publication",
            "cds-datatake",
        ],
        operation="update_by_query",
    )
    def migrate_linked_documents(self):
        dict_payload = {
            "query": {
                "query_string": {
                    "query": "last_attached_ticket: * OR last_attached_ticket_url: * OR cams_tickets: *"
                }
            },
            "script": """
            // Replace old urls with new url
            def url = ctx._source.last_attached_ticket_url;
            if (url != null) {
                url = url.substring(30); // Remove old url
                url = "https://esa-cams.atlassian.net/browse/" + url; // Add new url
                ctx._source.last_attached_ticket_url = url;
                }

            def last_ticket = ctx._source.last_attached_ticket;
            if (last_ticket != null && last_ticket.length() > 2) {
                last_ticket = last_ticket.substring(2); // Remove the first 2 characters
                ctx._source.last_attached_ticket = last_ticket;
            }

            // Process 'cams_tickets' list (list of ticket id)
            def cams_tickets = ctx._source.cams_tickets;
            if (cams_tickets != null) {
                for (int i = 0; i < cams_tickets.size(); i++) {
                    def item = cams_tickets[i];
                    if (item != null && item.length() > 2) {
                        item = item.substring(2); // Remove the first 2 characters
                        cams_tickets[i] = item;
                    }
                }
                ctx._source.cams_tickets = cams_tickets;
            }
            """,
        }
        yield dict_payload

    @payload_to_tasks(
        indexes=[
            "cds-product-2024-01",
            "cds-product-2023-12",
            "cds-publication-2024-01",
            "cds-publication-2023-12",
        ],
        operation="update_by_query",
    )
    def datatake_id_default_value(self):
        dict_payload = {
            "query": {"query_string": {"query": "NOT datatake_id: *"}},
            "script": "ctx._source.datatake_id= '______'",
        }
        yield dict_payload

    @payload_to_tasks(
        indexes=[
            "cds-product-2024-01",
            "cds-product-2023-12",
            "cds-publication-2024-01",
            "cds-publication-2023-12",
        ],
        operation="update_by_query",
    )
    def timeliness_default_value(self):
        dict_payload = {
            "query": {"query_string": {"query": "NOT timeliness: *"}},
            "script": "ctx._source.timeliness= '_'",
        }
        yield dict_payload

    @payload_to_tasks(
        indexes=[
            "cds-product-2024-01",
            "cds-product-2023-12",
            "cds-publication-2024-01",
            "cds-publication-2023-12",
        ],
        operation="update_by_query",
    )
    def product_level_default_value(self):
        dict_payload = {
            "query": {"query_string": {"query": "NOT product_level: *"}},
            "script": "ctx._source.product_level= '___'",
        }
        yield dict_payload

    ### OLD version

    @payload_to_tasks(
        indexes=["cds-product", "cds-publication"],
        operation="update_by_query",
    )
    def datatake_id_default_value_old(self):
        dict_payload = {
            "query": {
                "query_string": {
                    "query": "sensing_start_date: [* TO 2023-12-01T00:00:00.000Z] AND NOT datatake_id: *"
                }
            },
            "script": "ctx._source.datatake_id= '______'",
        }
        yield dict_payload

    @payload_to_tasks(
        indexes=["cds-product" "cds-publication"],
        operation="update_by_query",
    )
    def timeliness_default_value_old(self):
        dict_payload = {
            "query": {
                "query_string": {
                    "query": "sensing_start_date: [* TO 2023-12-01T00:00:00.000Z] AND NOT datatake_id: *"
                }
            },
            "script": "ctx._source.timeliness= '_'",
        }
        yield dict_payload

    @payload_to_tasks(
        indexes=["cds-product-2024-01", "cds-publication"],
        operation="update_by_query",
    )
    def product_level_default_value_old(self):
        dict_payload = {
            "query": {
                "query_string": {
                    "query": "sensing_start_date: [* TO 2023-12-01T00:00:00.000Z] AND NOT datatake_id: *"
                }
            },
            "script": "ctx._source.product_level= '___'",
        }
        yield dict_payload

    def run(self):
        """override"""

        self.tasks.set_connection(self.es_conn)

        self.migrate_cams_index()

        self.migrate_linked_documents()

        self.tasks.monitor(5)

        self.datatake_id_default_value()

        self.tasks.monitor(5)

        self.timeliness_default_value()

        self.tasks.monitor(5)

        self.product_level_default_value()

        self.tasks.monitor(5)

        ####

        # self.datatake_id_default_value_old()

        # self.tasks.monitor(1000)

        # self.timeliness_default_value_old()

        # self.tasks.monitor(1000)

        # self.product_level_default_value_old()

        # self.tasks.monitor(1000)


def run():
    migration_main(sys.argv[1:], PatchV2_2_2)


if __name__ == "__main__":
    run()
