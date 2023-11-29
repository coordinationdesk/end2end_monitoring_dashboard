#!/usr/bin/env python3
"""

Migration script to migrate CDS from 1.0.0 to 1.1.0
"""
import sys

from maas_engine.update.migration import MaasMigrator, migration_main

from maas_cds import model


class PatchV1_1_0(MaasMigrator):
    """Migration tool to migrate from 1.0.0 to 1.1.0"""

    @MaasMigrator.migration_action_iterator
    def migrate_datatake_id_iterator(self):
        """
        Migrate datatake document identifier to satellite_unit-datatake_id format and
        purge dynamic fields
        """

        search_request = (
            model.CdsDatatake.search().query().params(ignore=404, version=True)
        )

        for datatake in search_request.scan():

            if not datatake.meta.id.startswith(datatake.satellite_unit):

                datatake.purge_dynamic_fields()

                new_id = f"{datatake.satellite_unit}-{datatake.datatake_id}"

                datatake.key = new_id

                yield datatake.to_bulk_action(
                    "create",
                    _id=new_id,
                )

                yield datatake.to_bulk_action("delete")

    def run(self):
        """override"""
        # migrate datatake data to the new datatake identifier format
        self.bulk_exec(self.migrate_datatake_id_iterator())

        # migrate the mp index because of data type changes
        self.migrate_index_template("raw-data-mp-product")

        # migrate the datatake index because of data type changes
        self.migrate_index_template("cds-datatake")

        # migrate the cds-product index because of data type changes
        self.install_index("cds-product")

        # migrate the cds-product index because of data type changes
        self.install_index("cds-publication")


def run():
    migration_main(sys.argv[1:], PatchV1_1_0)


if __name__ == "__main__":
    run()
