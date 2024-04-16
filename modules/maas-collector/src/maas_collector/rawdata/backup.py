"""Ingested files backup"""

import dataclasses
import datetime
import gzip
import logging
import os
import shutil

import paramiko
import boto3
import botocore


@dataclasses.dataclass
class BackupArgs:
    """store backup parameters"""

    backup_type: str

    host: str

    port: str

    username: str

    password: str

    directory: str

    calendar_tree: bool

    enable_gzip: bool

    s3_endpoint: str

    s3_key_id: str

    s3_access_key: str

    s3_bucket: str


def instanciate_collector_backup(args: BackupArgs):
    """Instanciate the collector backup depending on argument given by user

    Raises:
        ValueError: Raised if user has given a wrong backup type as argument

    Returns:
        CollectorBackupS3 | CollectorBackupSFTP: CollectorBackup instanciated
    """
    if args.backup_type == "S3":
        return CollectorBackupS3(args)
    elif args.backup_type == "SFTP":
        return CollectorBackupSFTP(args)
    else:
        raise ValueError(f"Unknown Backup Type: {args.backup_type}")


class CollectorBackup:
    """Main Collector Backup class which contains all
    methods common to all backup implementations.
    This class shall not be instanciated but inherited"""

    DO_NOT_COMPRESS_EXTENSION = (".xlsx", ".gzip", ".zip")

    def __init__(self, args: BackupArgs):
        self.args = args
        self.logger = logging.getLogger(self.__class__.__name__)
        self.validate_backup_arguments()

    def close(self):
        """close transport and clear directory creation cache"""
        # Abstract Class
        raise NotImplementedError()

    def get_backup_path(
        self, config, path, dirdatetime: datetime.datetime = None
    ) -> tuple:
        """generate remote path"""

        path_elements = [self.args.directory]

        if self.args.calendar_tree:
            # DOI instead of ingestion time ?
            if dirdatetime is None:
                dirdatetime = datetime.datetime.utcnow()

            path_elements.extend(
                [
                    f"{dirdatetime.year:04d}",
                    f"{dirdatetime.month:02d}",
                    f"{dirdatetime.day:02d}",
                ]
            )

        if config.interface_name:
            path_elements.append(config.interface_name)
        else:
            # default: model class name. may be rabbit queue mmm ?
            path_elements.append(config.model_name)

        return "/".join(path_elements), os.path.basename(path)

    def backup_file(self, config, path):
        """Copy file to backup space

        Args:
            config (CollectorConfiguration): ingestion config
            path (str): local file path on the pod working directory
        """
        compression_enabled = self.args.enable_gzip
        for filetype in CollectorBackup.DO_NOT_COMPRESS_EXTENSION:
            if path.endswith(filetype):
                self.logger.debug(
                    "The following file %s will not be compressed before"
                    " being backed-up as its type '%s' in not suitable for compression",
                    path,
                    filetype,
                )
                compression_enabled = False
                break

        # handle compression.
        if compression_enabled:

            gzip_path = f"{path}.gz"

            self.logger.debug("Compressing %s to %s", path, gzip_path)

            with open(path, "rb") as f_in:

                with gzip.open(gzip_path, "wb") as f_out:

                    shutil.copyfileobj(f_in, f_out)

            path = gzip_path

        self.backup_file_implementation(config, path)

        # clean up compressed file
        if compression_enabled:
            os.remove(path)

    def backup_file_implementation(self, config, path):
        """This function which shall be redefined by the child class is responsible
           to perform the file backup operation to the remote server

        Args:
            config (CollectorConfiguration): ingestion config
            path (str): local file path on the pod working directory

        Raises:
            NotImplementedError: Raise in case the backup implementation
            function has not been defined in the instanciated child class
        """
        # Abstract Class
        raise NotImplementedError()

    def validate_backup_arguments(self):
        """Function used to make sure that all needed variables
        needed by the backup implementation have been provided
        """
        # Abstract Class
        raise NotImplementedError()


class CollectorBackupS3(CollectorBackup):
    """S3 implementation of the Collector Backup

    Args:
        CollectorBackup (CollectorBackup): Main Backup Collector Class
    """

    def __init__(self, args: BackupArgs):
        super().__init__(args)

        self.s3_client = boto3.client(
            service_name="s3",
            endpoint_url=self.args.s3_endpoint,
            aws_access_key_id=self.args.s3_key_id,
            aws_secret_access_key=self.args.s3_access_key,
        )

    def validate_backup_arguments(self):
        """Function used to make sure that all needed variables
        needed by the backup implementation have been provided

        Raises:
            ValueError: Raise if mandatory arguments needed for S3 backup are missing
        """
        if (
            not self.args.s3_endpoint
            or not self.args.s3_key_id
            or not self.args.s3_access_key
            or not self.args.s3_bucket
        ):
            raise ValueError(
                "The following arguments are mandatory for a S3 Backup"
                " logic => (backup-s3-endpoint, backup-s3-key-id,"
                " backup-s3-access-key, backup-s3-bucket)"
            )

    def close(self):
        # No action needed with S3 when transfert is over
        pass

    def backup_file_implementation(self, config, path):
        try:
            remote_file_path = "/".join(self.get_backup_path(config, path))

            self.logger.debug(
                "A backup of %s will be created on %s, its remote path will be %s",
                path,
                self.args.s3_bucket,
                remote_file_path,
            )

            self.s3_client.upload_file(path, self.args.s3_bucket, remote_file_path)
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
            boto3.exceptions.Boto3Error,
        ) as error:

            self.logger.critical(
                "Cannot backup file %s to %s on bucket %s due to the following error: %s",
                path,
                self.args.s3_endpoint,
                self.args.s3_bucket,
                error,
            )


class CollectorBackupSFTP(CollectorBackup):
    """store ingested files to an stfp server"""

    def __init__(self, args: BackupArgs):
        super().__init__(args)

        self.__transport: paramiko.Transport = None

        # a cache list of created directories to minimize sftp stat usage
        self._created_directories = []

    @property
    def transport(self):
        """property holding a lazy-created paramiko Transport"""

        if self.__transport is None or not self.__transport.is_active():

            self.logger.debug("Connecting to backup host %s", self.args.host)

            transport = paramiko.Transport((self.args.host, self.args.port))

            transport.connect(username=self.args.username, password=self.args.password)

            # send keep alive packet every 30 seconds
            transport.set_keepalive(30)

            self.__transport = transport

        return self.__transport

    def validate_backup_arguments(self):
        """Function used to make sure that all needed variables
        needed by the backup implementation have been provided

        Raises:
            ValueError: Raise if mandatory arguments needed for SFTP backup are missing
        """
        if (
            not self.args.host
            or not self.args.port
            or not self.args.username
            or not self.args.password
        ):
            raise ValueError(
                "The following arguments are mandatory for a SFTP Backup"
                " logic => (backup-hostname, backup-port, backup-username, backup-password)"
            )

    def makedirs(self, client: paramiko.SFTPClient, path: str):
        """create directory tree recursively

        Args:
            client (paramiko.SFTPClient): sftp client
            path (str): directory path
        """
        subdir = self.args.directory

        for subpath in path[len(self.args.directory) + 1 :].split("/"):

            subdir = "/".join([subdir, subpath])

            try:
                if subdir not in self._created_directories:
                    self.logger.debug("Checking if %s exists", subdir)
                    client.stat(subdir)

            except FileNotFoundError:
                self.logger.debug("Creating %s", subdir)
                client.mkdir(subdir)

            self._created_directories.append(subdir)

    def backup_file_implementation(self, config, path):
        """Copy file to backup space

        Args:
            config (CollectorConfiguration): ingestion config
            path (str): local file path on the pod working directory
        """

        try:
            # TODO may be retry n times
            with paramiko.SFTPClient.from_transport(self.transport) as client:

                target_dir, target_path = self.get_backup_path(config, path)

                self.logger.debug("Backuping %s to %s", path, target_path)

                if target_dir not in self._created_directories:

                    self.makedirs(client, target_dir)

                target = "/".join([target_dir, target_path])

                tmp_target = "/".join([target_dir, f".{target_path}"])

                self.logger.debug("Uploading %s to %s", path, tmp_target)

                client.put(path, tmp_target)

                self.logger.debug("Renaming %s to %s", tmp_target, target)

                client.posix_rename(tmp_target, target)

        except (paramiko.SSHException, IOError, OSError) as error:
            self.logger.critical("Cannot backup file %s to %s", path, self.args.host)
            self.logger.exception(error)
            # do not raise as logging critical is the only thing to do to not break
            # the ingestion loop

    def close(self):
        """close transport and clear directory creation cache"""
        if self.__transport:
            self.logger.debug("Closing backup sftp connection to %s", self.args.host)
            self.__transport.close()
            self.__transport = None

        self._created_directories.clear()
