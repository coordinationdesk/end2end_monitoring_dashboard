import argparse
import logging
import sys
from maas_model.date_utils import datestr_to_zulu
from opensearchpy.connection.connections import connections as es_connections

from maas_cds.model import MaasConfigCompleteness

from maas_engine.cli import args as maas_args


configs = [
    {
        "satellite_unit": "S1C",
        "prip_name": "S1C-Werum",
        "activated": True,
        "start_date": datestr_to_zulu("2024-12-01T00:00:00.000Z"),
        "end_date": datestr_to_zulu("2030-12-01T00:00:00.000Z"),
    },
    {
        "satellite_unit": "S1C",
        "prip_name": "S1C-Serco",
        "activated": True,
        "start_date": datestr_to_zulu("2024-12-01T00:00:00.000Z"),
        "end_date": datestr_to_zulu("2030-12-01T00:00:00.000Z"),
    },
]


def update_config():

    for config in configs:
        config_doc = MaasConfigCompleteness(**config)

        # put this in class model
        config_doc.key = f"{config_doc.satellite_unit}-{config_doc.prip_name}"

        old_config_doc = MaasConfigCompleteness.get_by_id(config_doc.key)

        if old_config_doc:
            config_doc = old_config_doc  # keep old refer
            config_doc._from_dict(config)
        else:
            config_doc.meta.id = config_doc.key

        config_doc.full_clean()

        print("save ", config_doc.meta.id)
        config_doc.save(refresh=True)


def update_config_main(argv):
    """commun entry point with args parsing

    Args:
        argv (list): argument provide to run satruman
    """

    # AMQP / ES access
    parser = argparse.ArgumentParser(parents=[maas_args.es_parser()])
    args = parser.parse_args(argv)

    es_url = maas_args.get_es_credentials_url(args)

    es_connections.create_connection(
        hosts=[es_url],
        retry_on_timeout=True,
        max_retries=args.es_retries,
        timeout=args.es_timeout,
        verify_certs=not args.es_ignore_certs_verification,
        ssl_show_warn=not args.es_ignore_certs_verification,
    )

    # shut up opensearchpy
    logging.getLogger("opensearchpy").setLevel(logging.WARNING)

    update_config()


def run():
    """main entry point"""
    update_config_main(sys.argv[1:])


if __name__ == "__main__":
    run()
