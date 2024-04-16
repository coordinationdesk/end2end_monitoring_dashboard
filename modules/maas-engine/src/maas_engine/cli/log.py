"""logging related stuff"""
import logging
import sys


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s: %(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )

    # lower verbosity of third party components to ease debug in development
    # can be customized in configuration file
    if loglevel == logging.DEBUG:
        for name in (
            # "urllib3.connectionpool",
            "opensearch",
            "amqp",
            "botocore.auth",
            "botocore.client",
            "boto3.resources.factory",
            "boto3.resources.model",
            "botocore.parsers",
            "botocore.loaders",
            "botocore.retryhandler",
            "botocore.hooks",
            "botocore.endpoint",
            "botocore.utils",
            "s3transfer.tasks",
            "s3transfer.futures",
            "s3transfer.utils",
            "paramiko.transport",
            # "paramiko.transport.sftp",
        ):
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)

        logging.getLogger("requests").setLevel(logging.DEBUG)
