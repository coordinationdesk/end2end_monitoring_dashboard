"""tools for command line interface"""

import logging
import os
import urllib
from argparse import Action, ArgumentParser, Namespace

import maas_collector

from maas_collector.rawdata.backup import BackupArgs
from maas_collector.rawdata.replay import ReplayArgs


class EnvDefault(Action):
    """argparse.Action that gets value from environment"""

    def __init__(self, envvar, required=True, default=None, **kwargs):
        if envvar in os.environ:
            default = os.environ[envvar]
        if required and default:
            required = False
        super().__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def es_parser() -> ArgumentParser:
    """opensearch CLI argument parser factory

    Returns:
        ArgumentParser: opensearch argument parser

    """
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "--es-username",
        dest="es_username",
        help="opensearch user identifier (default: %(default)s)",
        action=EnvDefault,
        envvar="ES_USERNAME",
        required=False,
        type=str,
    )
    parser.add_argument(
        "--es-password",
        dest="es_password",
        help="opensearch user password (default: %(default)s)",
        action=EnvDefault,
        envvar="ES_PASSWORD",
        required=False,
        type=str,
    )
    parser.add_argument(
        "--es-url",
        dest="es_url",
        help="opensearch cluster URL (default: %(default)s)",
        action=EnvDefault,
        envvar="ES_URL",
        required=False,
        type=str,
    )
    parser.add_argument(
        "--es-timeout",
        dest="es_timeout",
        help="opensearch request timeout in seconds (default: %(default)s)",
        action=EnvDefault,
        envvar="ES_TIMEOUT",
        required=False,
        default=120,
        type=int,
    )
    parser.add_argument(
        "--es-retries",
        dest="es_retries",
        help="opensearch number of retries (default: %(default)s)",
        action=EnvDefault,
        envvar="ES_RETRIES",
        required=False,
        default=3,
        type=int,
    )

    parser.add_argument(
        "--es-ignore-certs-verification",
        dest="es_ignore_certs_verification",
        help="If set, the SSL cert of opensearch is not verified (default: %(default)s)",
        action=EnvDefault,
        envvar="IGNORE_CERTS_VERIFICATION",
        required=False,
        type=bool,
        default=False,
    )

    return parser


def get_es_credentials_url(namespace: Namespace) -> str:
    """get final url for opensearch connection

    Args:
        namespace (Namespace): result of ArgParser.parse()

    Returns:
        str: full connection url
    """
    return get_credentials_url(
        namespace.es_url, namespace.es_username, namespace.es_password
    )


def amqp_parser() -> ArgumentParser:
    """AMQP CLI argument parser factory

    Returns:
        ArgumentParser: AMQP argument parser

    """
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "--amqp-username",
        dest="amqp_username",
        help="AMQP user name (default: %(default)s)",
        action=EnvDefault,
        envvar="AMQP_USERNAME",
        required=False,
        type=str,
    )
    parser.add_argument(
        "--amqp-password",
        dest="amqp_password",
        help="AMQP user password (default: %(default)s)",
        action=EnvDefault,
        envvar="AMQP_PASSWORD",
        required=False,
        type=str,
    )
    parser.add_argument(
        "--amqp-url",
        dest="amqp_url",
        help="AMQP cluster URL (default: %(default)s)",
        action=EnvDefault,
        envvar="AMQP_URL",
        required=False,
        type=str,
    )
    parser.add_argument(
        "--amqp-retries",
        dest="amqp_retries",
        help="AMQP number of retries (default: %(default)s). 0 for infinite",
        action=EnvDefault,
        envvar="AMQP_RETRIES",
        required=False,
        default=0,
        type=int,
    )
    parser.add_argument(
        "--amqp-priority",
        dest="amqp_priority",
        help="AMQP message priority (default: %(default)s). higher is higher priority",
        action=EnvDefault,
        envvar="AMQP_PRIORITY",
        required=False,
        default=5,
        type=int,
    )
    return parser


def s3_parser():
    """S3 CLI argument parser factory

    Returns:
        ArgumentParser: S2 argument parser

    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--s3-endpoint",
        dest="s3_endpoint",
        help="S3 endpoint URL (default: %(default)s)",
        action=EnvDefault,
        envvar="S3_ENDPOINT",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--s3-key-id",
        dest="s3_key_id",
        help="S3 key identifier (default: %(default)s)",
        action=EnvDefault,
        envvar="S3_KEY_ID",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--s3-access-key",
        dest="s3_access_key",
        help="S3 access key  (default: %(default)s)",
        action=EnvDefault,
        envvar="S3_ACCESS_KEY",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--s3-bucket",
        dest="s3_bucket",
        help="S3 bucket  (default: %(default)s)",
        action=EnvDefault,
        envvar="S3_BUCKET",
        required=False,
        type=str,
    )

    # sooner or later options
    # S3 related but could be combined with sftp ingestion
    # parser.add_argument(
    #     "--error-bucket",
    #     dest="error_bucket",
    #     help="Error bucket to store inconsistant files (default: %(default)s)",
    #     action=EnvDefault,
    #     envvar="S3_ERROR_BUCKET",
    #     required=False,
    #     default=""
    #     type=str,
    # )

    # S3 related but could be combined with sftp ingestion
    # parser.add_argument(
    #     "--archive-bucket",
    #     dest="archive_bucket",
    #     help="Archive bucket to store processed files (default: %(default)s)",
    #     action=EnvDefault,
    #     envvar="S3_ARCHIVE_BUCKET",
    #     required=False,
    #     type=str,
    # )

    return parser


def sftp_parser():
    """SFTP CLI argument parser factory

    Returns:
        ArgumentParser: SFTP argument parser

    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--sftp-hostname",
        dest="sftp_hostname",
        help="SFTP host name (default: %(default)s)",
        action=EnvDefault,
        envvar="SFTP_HOSTNAME",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--sftp-port",
        dest="sftp_port",
        help="SFTP port(default: %(default)s)",
        action=EnvDefault,
        envvar="SFTP_PORT",
        required=False,
        type=int,
        default=22,
    )

    parser.add_argument(
        "--sftp-username",
        dest="sftp_username",
        help="SFTP user name (default: %(default)s)",
        action=EnvDefault,
        envvar="SFTP_USERNAME",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--sftp-password",
        dest="sftp_password",
        help="SFTP user password (default: %(default)s)",
        action=EnvDefault,
        envvar="SFTP_PASSWORD",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--sftp-process-prefix",
        dest="sftp_process_prefix",
        help="File prefix for processing file (default: %(default)s)",
        action=EnvDefault,
        envvar="SFTP_PROCESS_PREFIX",
        required=False,
        type=str,
        default=".maas-process-",
    )

    parser.add_argument(
        "--sftp-inbox-root",
        dest="sftp_inbox_root",
        help="Inbox root directory to store INGESTED and REJECTED "
        "directories (default: %(default)s)",
        action=EnvDefault,
        envvar="SFTP_INBOX_ROOT",
        required=False,
        type=str,
        default="",
    )

    parser.add_argument(
        "--sftp-ingested-dir",
        dest="sftp_ingested_dir",
        help="Directory to store successfully ingested files (default: %(default)s)",
        action=EnvDefault,
        envvar="SFTP_INGESTED_DIR",
        required=False,
        type=str,
        default="INGESTED",
    )

    parser.add_argument(
        "--sftp-rejected-dir",
        dest="sftp_rejected_dir",
        help="Directory to store rejected files (default: %(default)s)",
        action=EnvDefault,
        envvar="SFTP_REJECTED_DIR",
        required=False,
        type=str,
        default="REJECTED",
    )

    parser.add_argument(
        "--sftp-force-suffix",
        dest="sftp_force_suffix",
        help="File suffix for forcing file ingestion (default: %(default)s)",
        action=EnvDefault,
        envvar="SFTP_FORCE_SUFFIX",
        required=False,
        type=str,
        default=".MAAS-FORCE",
    )

    parser.add_argument(
        "--sftp-age-limit",
        dest="sftp_age_limit",
        help="Age limit in seconds for a file to be considered abandonned and "
        + "ingested again (default: %(default)s seconds)",
        action=EnvDefault,
        envvar="SFTP_AGE_LIMIT",
        required=False,
        type=int,
        default=15 * 60,
    )

    return parser


def jira_parser():
    """Jira CLI argument parser factory

    Returns:
        ArgumentParser: Jira argument parser

    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--jira-endpoint",
        dest="jira_endpoint",
        help="JIRA endpoint (default: %(default)s)",
        action=EnvDefault,
        envvar="JIRA_ENDPOINT",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--jira-username",
        dest="jira_username",
        help="JIRA user name (default: %(default)s)",
        action=EnvDefault,
        envvar="JIRA_USERNAME",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--jira-token",
        dest="jira_token",
        help="JIRA user token (default: %(default)s)",
        action=EnvDefault,
        envvar="JIRA_TOKEN",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--jira-auth-method",
        dest="jira_auth_method",
        help="JIRA authentication method (['bearer','auth'], default: %(default)s)",
        action=EnvDefault,
        envvar="JIRA_AUTH_METHOD",
        required=False,
        type=str,
    )

    return parser


def weather_parser():
    """Weather CLI argument parser factory

    Returns:
        ArgumentParser: Weather argument parser

    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--weather-timeout",
        dest="weather_timeout",
        help="Default timeout (default: %(default)s)",
        action=EnvDefault,
        envvar="Weather_TIMEOUT",
        required=False,
        type=int,
        default=120,
    )

    parser.add_argument(
        "--weather-keep-files",
        dest="weather_keep_files",
        help="Keep downloaded api pages (default: %(default)s)",
        action=EnvDefault,
        envvar="Weather_KEEP_FILES",
        required=False,
        type=bool,
        default=False,
    )

    return parser


def odata_parser():
    """OData CLI argument parser factory

    Returns:
        ArgumentParser: OData argument parser

    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--odata-timeout",
        dest="odata_timeout",
        help="Default timeout (default: %(default)s)",
        action=EnvDefault,
        envvar="ODATA_TIMEOUT",
        required=False,
        type=int,
        default=120,
    )

    parser.add_argument(
        "--odata-keep-files",
        dest="odata_keep_files",
        help="Keep downloaded api pages (default: %(default)s)",
        action=EnvDefault,
        envvar="ODATA_KEEP_FILES",
        required=False,
        type=bool,
        default=False,
    )

    return parser


def s3_parser():
    """S3 CLI argument parser factory

    Returns:
        ArgumentParser: S3 argument parser

    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--s3-timeout",
        dest="s3_timeout",
        help="Default timeout (default: %(default)s)",
        action=EnvDefault,
        envvar="S3_TIMEOUT",
        required=False,
        type=int,
        default=120,
    )

    parser.add_argument(
        "--s3-keep-files",
        dest="s3_keep_files",
        help="Keep downloaded api pages (default: %(default)s)",
        action=EnvDefault,
        envvar="S3_KEEP_FILES",
        required=False,
        type=bool,
        default=False,
    )

    return parser


def loki_parser():
    """Loki CLI argument parser factory

    Returns:
        ArgumentParser: Loki argument parser

    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--loki-timeout",
        dest="loki_timeout",
        help="Default timeout (default: %(default)s)",
        action=EnvDefault,
        envvar="LOKI_TIMEOUT",
        required=False,
        type=int,
        default=120,
    )

    parser.add_argument(
        "--loki-keep-files",
        dest="loki_keep_files",
        help="Keep downloaded api pages (default: %(default)s)",
        action=EnvDefault,
        envvar="LOKI_KEEP_FILES",
        required=False,
        type=bool,
        default=False,
    )

    return parser


def mpip_parser():
    """Mpip CLI argument parser factory

    Returns:
        ArgumentParser: Mpip argument parser

    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--mpip-timeout",
        dest="mpip_timeout",
        help="Default timeout (default: %(default)s)",
        action=EnvDefault,
        envvar="MPIP_TIMEOUT",
        required=False,
        type=int,
        default=120,
    )

    parser.add_argument(
        "--mpip-keep-files",
        dest="mpip_keep_files",
        help="Keep downloaded api pages (default: %(default)s)",
        action=EnvDefault,
        envvar="MPIP_KEEP_FILES",
        required=False,
        type=bool,
        default=False,
    )

    return parser


def webdav_parser():
    """WebDAV CLI argument parser factory

    Returns:
        ArgumentParser: WebDAV argument parser

    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--webdav-timeout",
        dest="webdav_timeout",
        help="Default timeout (default: %(default)s)",
        action=EnvDefault,
        envvar="WEBDAV_TIMEOUT",
        required=False,
        type=int,
        default=120,
    )

    return parser


def get_amqp_credentials_url(namespace: Namespace) -> str:
    """get final url for AMQP connection

    Args:
        namespace (Namespace): result of ArgParser.parse()

    Returns:
        str: full connection url
    """
    return get_credentials_url(
        namespace.amqp_url, namespace.amqp_username, namespace.amqp_password
    )


def get_credentials_url(url: str, username: str, password: str) -> str:
    """Add credentials to an url

    Args:
        url (str): enpoint url
        username (str): user name
        password (str): user password

    Returns:
        str: url with credentials
    """

    new_url = None
    if not username:
        new_url = url
    elif url:
        # parse arg url
        parse_result = urllib.parse.urlparse(url)
        # extract domain name
        domain = parse_result.netloc.split("@")[-1]
        new_username = parse_result.username
        new_password = parse_result.password
        # init credentials if provided in url and not override by args
        if username:
            new_username = username
        if password:
            new_password = password
        # Format the complete url with credentials
        new_url = (
            f"{parse_result.scheme}://{new_username}:{new_password}"
            f"@{domain}{parse_result.path}"
        )
    return new_url


def backup_parser_s3():
    """Specific S3 backup parameters CLI argument parser factory

    Returns:
        ArgumentParser: Specific S3 backup parameters argument parser

    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--backup-s3-endpoint",
        dest="backup_s3_endpoint",
        help="Backup S3 endpoint URL (default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_S3_ENDPOINT",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--backup-s3-key-id",
        dest="backup_s3_key_id",
        help="Backup S3 key identifier (default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_S3_KEY_ID",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--backup-s3-access-key",
        dest="backup_s3_access_key",
        help="Backup S3 access key  (default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_S3_ACCESS_KEY",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--backup-s3-bucket",
        dest="backup_s3_bucket",
        help="Backup S3 bucket  (default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_S3_BUCKET",
        required=False,
        type=str,
    )

    return parser


def backup_parser_general():
    """Common backup parameters CLI argument parser factory

    Returns:
        ArgumentParser: Common backup parameters argument parser

    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "-b",
        "--backup",
        dest="backup_enabled",
        help="Enable backup (default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_ENABLED",
        required=False,
        default=False,
        type=bool,
    )

    parser.add_argument(
        "-bt",
        "--backup_type",
        dest="backup_type",
        help="Choose backup type to use (default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_TYPE",
        required=False,
        default="SFTP",
        type=str,
        choices=["SFTP", "S3"],
    )

    parser.add_argument(
        "--backup-dir",
        dest="backup_dir",
        help="Backup directory (default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_DIR",
        required=False,
        type=str,
        default="",
    )

    parser.add_argument(
        "--backup-calendar-tree",
        dest="backup_calendar_tree",
        help="Create YYYY/MM/DD backup file tree (default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_CALENDAR_TREE",
        required=False,
        default=False,
        type=bool,
    )

    parser.add_argument(
        "--backup-gzip",
        dest="backup_gzip",
        help="Compress backup with gzip (default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_GZIP",
        required=False,
        default=False,
        type=bool,
    )

    return parser


def backup_parser_sftp():
    """Specific SFTP backup parameters CLI argument parser factory

    Returns:
        ArgumentParser: Specific SFTP backup parameters argument parser

    """
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "--backup-hostname",
        dest="backup_hostname",
        help="Backup host name (default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_HOSTNAME",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--backup-port",
        dest="back_port",
        help="Backup host port(default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_PORT",
        required=False,
        type=int,
        default=22,
    )

    parser.add_argument(
        "--backup-username",
        dest="backup_username",
        help="Backup user name (default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_USERNAME",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--backup-password",
        dest="backup_password",
        help="Backup user password (default: %(default)s)",
        action=EnvDefault,
        envvar="BACKUP_PASSWORD",
        required=False,
        type=str,
    )
    return parser


def replay_parser() -> ArgumentParser:
    """parser factory for replay arguments

    Returns:
        ArgumentParser: replay argument parser
    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--replay-interface-name",
        dest="replay_interface_name",
        help="Enable Collect Replay on these interfaces (default: %(default)s)",
        action=EnvDefault,
        envvar="REPLAY_INTERFACE_NAME",
        required=False,
        default="",
        type=str,
        nargs="+",
    )

    parser.add_argument(
        "--replay-start-date",
        dest="replay_start_date",
        help="Start datetime of the replay in ZULU format (default: %(default)s)",
        action=EnvDefault,
        envvar="REPLAY_START_DATE",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--replay-end-date",
        dest="replay_end_date",
        help="End datetime of the replay in ZULU format (default: %(default)s)",
        action=EnvDefault,
        envvar="REPLAY_END_DATE",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--replay-suffix",
        dest="replay_suffix",
        help="This field allow us to have multiple replay for a "
        "single interface_name (default: %(default)s)",
        action=EnvDefault,
        envvar="REPLAY_SUFFIX",
        required=False,
        default="",
        type=str,
    )

    parser.add_argument(
        "--replay-retry",
        dest="replay_retry",
        help="Number of retry (default: %(default)s)",
        action=EnvDefault,
        envvar="REPLAY_RETRY",
        required=False,
        default=1024,
        type=int,
    )

    return parser


def common_parser() -> ArgumentParser:
    """common cli parser factory

    Returns:
        ArgumentParser: common argument parser
    """
    parser = ArgumentParser(
        add_help=False,
        parents=[
            es_parser(),
            amqp_parser(),
            backup_parser_general(),
            backup_parser_s3(),
            backup_parser_sftp(),
            replay_parser(),
        ],
    )

    parser.add_argument(
        "-f", "--force", action="store_true", help="Force rawdata update", default=False
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="Activate verbose mode",
        action="store_const",
        const=logging.INFO,
    )

    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"maas_collector {maas_collector.__version__}",
    )

    parser.add_argument(
        "-c",
        "--rawdata-config",
        dest="rawdata_config",
        help="Raw data configuration path (default: %(default)s)",
        action=EnvDefault,
        envvar="RAWDATA_CONFIG",
        required=False,
        type=str,
    )

    parser.add_argument(
        "-d",
        "--rawdata-config-directory",
        dest="rawdata_config_dir",
        help="Raw data configuration directory (default: %(default)s)",
        action=EnvDefault,
        envvar="RAWDATA_CONFIG_DIR",
        required=False,
        type=str,
    )

    parser.add_argument(
        "-p",
        "--watch-period",
        dest="watch_period",
        help="Watch period for filesystem and sftp (default: %(default)s)",
        action=EnvDefault,
        envvar="WATCH_PERIOD",
        required=False,
        type=int,
        default=60,
    )

    parser.add_argument(
        "--working-directory",
        dest="working_directory",
        help="Directory for sftp and s3 downloads (default: %(default)s)",
        action=EnvDefault,
        envvar="WORKING_DIR",
        required=False,
        type=str,
        default="/tmp",
    )

    parser.add_argument(
        "--healthcheck-hostname",
        dest="healthcheck_hostname",
        help="Health check host name (default: %(default)s)",
        action=EnvDefault,
        envvar="HEALTHCHECK_HOSTNAME",
        required=False,
        type=str,
        default="0.0.0.0",
    )

    parser.add_argument(
        "--healthcheck-port",
        dest="healthcheck_port",
        help="Health check port (default: %(default)s)",
        action=EnvDefault,
        envvar="HEALTHCHECK_PORT",
        required=False,
        type=int,
        default=80,
    )

    parser.add_argument(
        "--healthcheck-timeout",
        dest="healthcheck_timeout",
        help="Time before set status to error in seconds. (default: %(default)s)",
        action=EnvDefault,
        envvar="HEALTHCHECK_TIMEOUT",
        required=False,
        type=int,
        default=1800,
    )

    parser.add_argument(
        "--v1-compatibility",
        dest="v1_compatibility",
        help="V1 compatibility (default: %(default)s): simple amqp message payload",
        action="store_true",
        required=False,
        default=False,
    )

    parser.add_argument(
        "--force-message",
        dest="force_message",
        help="Notify unmodified documents on the amqp bus (default: %(default)s)",
        action="store_true",
        required=False,
        default=False,
    )

    parser.add_argument(
        "--credential-file",
        dest="credential_file",
        help="Credential file (default: %(default)s)",
        action=EnvDefault,
        envvar="CREDENTIAL_FILE",
        required=False,
        type=str,
    )

    return parser


def get_collector_args(classobj, namespace, **kwargs):
    """CollectorArgs factory

    Args:
        classobj ([CollectorArgs]): class to instanciate
        namespace ([NameSpace]): [description]

    Returns:
        [CollectorArgs]: args instance
    """
    args = classobj(
        es_url=get_es_credentials_url(namespace),
        es_timeout=namespace.es_timeout,
        es_ignore_certs_verification=namespace.es_ignore_certs_verification,
        amqp_url=get_amqp_credentials_url(namespace),
        rawdata_config=namespace.rawdata_config,
        rawdata_config_dir=namespace.rawdata_config_dir,
        force=namespace.force,
        working_directory=namespace.working_directory,
        healthcheck_hostname=namespace.healthcheck_hostname,
        healthcheck_port=namespace.healthcheck_port,
        healthcheck_timeout=namespace.healthcheck_timeout,
        watch_period=namespace.watch_period,
        v1_compatibility=namespace.v1_compatibility,
        es_retries=namespace.es_retries,
        amqp_retries=namespace.amqp_retries,
        force_message=namespace.force_message,
        credential_file=namespace.credential_file,
        amqp_priority=namespace.amqp_priority,
        **kwargs,
    )

    # setup backup configuration
    if namespace.backup_enabled:
        args.backup = BackupArgs(
            namespace.backup_type,
            namespace.backup_hostname,
            namespace.back_port,
            namespace.backup_username,
            namespace.backup_password,
            namespace.backup_dir,
            namespace.backup_calendar_tree,
            namespace.backup_gzip,
            namespace.backup_s3_endpoint,
            namespace.backup_s3_key_id,
            namespace.backup_s3_access_key,
            namespace.backup_s3_bucket,
        )

    if namespace.replay_interface_name:
        args.replay = ReplayArgs(
            namespace.replay_interface_name,
            namespace.replay_start_date,
            namespace.replay_end_date,
            namespace.replay_suffix,
            namespace.replay_retry,
        )
        if args.replay.start_date > args.replay.end_date:
            raise ValueError("Replay arguments: end date is inferior than start date !")

    if args.watch_period > args.healthcheck_timeout:
        new_timeout = args.watch_period + 10
        logging.warning(
            "Health Check Timeout value : %s is smaller than watch period value : %s"
            + " Health Check timeout value is set to watch period + 10s : %s",
            str(args.healthcheck_timeout),
            str(args.watch_period),
            str(new_timeout),
        )
        args.healthcheck_timeout = new_timeout

    return args


def http_common_parser():
    """Http CLI argument parser factory

    Returns:
        ArgumentParser: Http argument parser

    """
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--http-common-timeout",
        dest="http_common_timeout",
        help="Default timeout (default: %(default)s) in seconds",
        action=EnvDefault,
        envvar="HTTP_COMMON_TIMEOUT",
        required=False,
        type=int,
        default=120,
    )

    parser.add_argument(
        "--http-common-keep-files",
        dest="http_common_keep_files",
        help="Keep downloaded api pages (default: %(default)s)",
        action=EnvDefault,
        envvar="HTTP_COMMON_KEEP_FILES",
        required=False,
        type=bool,
        default=False,
    )

    return parser
