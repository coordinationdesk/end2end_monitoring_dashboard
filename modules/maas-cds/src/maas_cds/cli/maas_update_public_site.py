"""cli utility to update public site data"""
import argparse
import sys

from maas_engine.cli.args import engine_parser, s3_parser
from maas_engine.cli.run import maas_engine_main


def update_public_site(args):
    "engine call"

    # specific arguments for public dashboard
    public_dashboard_parser = argparse.ArgumentParser(add_help=False)

    public_dashboard_parser.add_argument(
        "-d", "--dryrun", action="store_true", help="Do not upload data", default=False
    )

    public_dashboard_parser.add_argument(
        "-o", "--output-dir", help="Save files to a local directory"
    )

    public_dashboard_parser.add_argument(
        "--pages",
        help="generate only specified data files",
        nargs="+",
    )

    public_dashboard_parser.add_argument(
        "-l",
        "--list",
        help="list available target files",
        action="store_true",
        default=False,
    )

    maas_engine_main(
        args,
        "PUBLIC_SITE_BACKEND",
        [engine_parser(), s3_parser(), public_dashboard_parser],
    )


def run():
    "main entry point"
    update_public_site(sys.argv[1:])


if __name__ == "__main__":
    run()
