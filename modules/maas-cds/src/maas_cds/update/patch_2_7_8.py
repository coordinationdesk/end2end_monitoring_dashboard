#!/usr/bin/env python3
"""

Migration script to migrate CDS from 2.2.0 to 2.2.2
"""

import sys
from maas_cds import model
from maas_engine.update.migration import MaasMigrator, migration_main
from maas_model import datestr_to_zulu


class PatchV2_7_8(MaasMigrator):

    @MaasMigrator.migration_action_iterator
    def init_completeness_config(self):
        """
        Init maas completeteness configuration
        """

        init_args = [
            {
                "prip_name": "S1C-Serco",
                "satellite_unit": "S1C",
                "activated": True,
                "start_date": datestr_to_zulu("2024-12-01T00:00:00.000Z"),
                "end_date": datestr_to_zulu("2099-01-01T00:00:00.000Z"),
            },
            {
                "prip_name": "S1C-Werum",
                "satellite_unit": "S1C",
                "activated": True,
                "start_date": datestr_to_zulu("2024-12-01T00:00:00.000Z"),
                "end_date": datestr_to_zulu("2099-01-01T00:00:00.000Z"),
            },
            {
                "prip_name": "S3B-SERCO",
                "satellite_unit": "S3B",
                "activated": True,
                "start_date": datestr_to_zulu("2024-12-01T00:00:00.000Z"),
                "end_date": datestr_to_zulu("2099-01-01T00:00:00.000Z"),
            },
            {
                "prip_name": "S3B-TPZ",
                "satellite_unit": "S3B",
                "activated": True,
                "start_date": datestr_to_zulu("2024-12-01T00:00:00.000Z"),
                "end_date": datestr_to_zulu("2099-01-01T00:00:00.000Z"),
            },
        ]
        for args in init_args:
            maas_config_document = model.MaasConfigCompleteness(**args)

            new_id = f"{maas_config_document.satellite_unit}-{maas_config_document.prip_name}"

            maas_config_document.key = new_id

            maas_config_document.full_clean()

            # Don't care about conflict

            yield maas_config_document.to_bulk_action(
                "create",
                _id=new_id,
            )

    def run(self):
        """override"""
        # create
        self.bulk_exec(self.init_completeness_config())


def run():
    migration_main(sys.argv[1:], PatchV2_7_8)


if __name__ == "__main__":
    run()
