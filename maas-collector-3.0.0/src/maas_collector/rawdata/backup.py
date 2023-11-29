"""Ingested files backup"""
import dataclasses
import datetime
import gzip
import logging
import os
import shutil

import paramiko


@dataclasses.dataclass
class BackupArgs:
    """store backup parameters"""

    host: str

    port: str

    username: str

    password: str

    directory: str

    calendar_tree: bool

    enable_gzip: bool


class CollectorBackup:
    """store ingested files to an stfp server"""

    def __init__(self, args: BackupArgs):
        self.args = args
        self.logger = logging.getLogger(self.__class__.__name__)

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

    def backup_file(self, config, path):
        """Copy file to backup space

        Args:
            config (CollectorConfiguration): ingestion config
            path (str): local file path on the pod working directory
        """

        # handle compression.
        if self.args.enable_gzip:

            # TODO Do not compress other archive files like gzip, xslx

            gzip_path = f"{path}.gz"

            self.logger.debug("Compressing %s to %s", path, gzip_path)

            with open(path, "rb") as f_in:

                with gzip.open(gzip_path, "wb") as f_out:

                    shutil.copyfileobj(f_in, f_out)

            path = gzip_path

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

        finally:
            # clean up compressed file
            if self.args.enable_gzip:
                os.remove(path)

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

    def close(self):
        """close transport and clear directory creation cache"""
        if self.__transport:
            self.logger.debug("Closing backup sftp connection to %s", self.args.host)
            self.__transport.close()
            self.__transport = None

        self._created_directories.clear()
