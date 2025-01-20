"""Extract files from SFTP server"""

from dataclasses import dataclass
import os
import time
import uuid

import pysftp

from maas_collector.rawdata.collector.filecollector import FileCollector, CollectorArgs

from maas_collector.rawdata.meta import IngestionMeta


# collector configuration class needs many attributes
# pylint: disable=R0902
@dataclass
class SFTPConfiguration:
    """Store SFTP configuration vars"""

    hostname: str

    port: int

    username: str

    password: str

    process_prefix: str

    inbox_root: str

    ingested_dir: str

    rejected_dir: str

    force_suffix: str

    age_limit: int


class SFTPCollector(FileCollector):
    """A collector that collect from a SFTP server"""

    CLEAN_UP_AGE_FACTOR = 0.8

    def __init__(
        self,
        args: CollectorArgs,
        sftp_config: SFTPConfiguration,
    ):
        super().__init__(args)
        self.sftp_config: SFTPConfiguration = sftp_config

        # file currently processed
        self._current_remote: str = None

        # pysftp connection
        self._sftp: pysftp.Connection = None

        # created directories to use makedirs() only when necessary
        self.__created_dirs = set()

        # a list of source / target
        self.__files_to_move_args = []

        # full processing prefix length, sum of:
        #  - length of the sftp_config.process_prefix string
        #  - 32 stands for uuid4 length
        #  - 1 for the separator
        self.__prefix_length = len(sftp_config.process_prefix) + 32 + 1

    @property
    def sftp(self) -> pysftp.Connection:
        """pysftp connection getter with lazy build
        Returns:
            [pysftp.Connection]: active pysftp connection
        """
        if self._sftp is None:
            # deactivate known hosts check. Bad idea
            cnopts = pysftp.CnOpts(knownhosts=None)
            cnopts.hostkeys = None
            self._sftp = pysftp.Connection(
                self.sftp_config.hostname,
                username=self.sftp_config.username,
                password=self.sftp_config.password,
                port=self.sftp_config.port,
                cnopts=cnopts,
            )
        return self._sftp

    def clear_sftp_connection(self):
        """Explicit connection shutdown"""
        self.__created_dirs.clear()
        if not self._sftp is None:
            self._sftp.close()
            self._sftp = None

    def __del__(self):
        self.clear_sftp_connection()

    def on_loop_end(self):
        """override"""
        self.clear_sftp_connection()

    def ingest(self, path: str, configs=None, force_update=False):
        """Ingest remote file or directory

        Args:
            path ([str]): list of relative path to sftp_config.inbox_root
        """

        self.logger.debug(
            "Looking for files in %s on %s", path, self.sftp_config.hostname
        )

        file_list = self.get_remote_file_list(path)

        meta_dict = {
            name[: -len(IngestionMeta.SUFFIX)]: name
            for name in file_list
            if name.endswith(IngestionMeta.SUFFIX)
        }

        file_list = [
            remote_path
            for remote_path in file_list
            if not remote_path.endswith(IngestionMeta.SUFFIX)
        ]

        self.logger.info("Real list : %s", file_list)

        for remote_path in file_list:
            self.ingest_sftp_file(
                remote_path,
                force_update=force_update,
                meta_path=meta_dict.get(remote_path),
            )

        self._flush_message_groups()

    def ingest_sftp_file(self, remote_path: str, force_update=False, meta_path=None):
        """Ingest a remote file

        Args:
            remote_path (str): remote file path
            force_update (bool, optional): force new document. Defaults to False.
        """
        self._healthcheck.tick()

        # handle forced update files
        # canonical_path stores the path without force_suffix so CollectorConfig
        # instances can be found
        if remote_path.endswith(self.sftp_config.force_suffix):
            # strip force suffix
            canonical_path = remote_path[: -len(self.sftp_config.force_suffix)]
            force_update = True
        else:
            canonical_path = remote_path

        # filter unhandled files
        configs = self.get_configurations(canonical_path)

        if not configs:
            self.logger.info("No rule matched : ignoring %s", remote_path)
            return

        try:
            dirname = os.path.dirname(remote_path)

            basename = os.path.basename(canonical_path)

            processed_path = os.path.join(
                dirname, self.get_processing_filename(basename)
            )

            # try renaming for exclusive processing
            try:
                self.logger.debug(
                    "Trying renaming %s to %s", remote_path, processed_path
                )

                self.sftp.rename(remote_path, processed_path)

                self.logger.debug("Successfully renamed")

            except (FileNotFoundError, OSError, IOError):
                if not self.sftp.isfile(remote_path):
                    self.logger.warning(
                        "%s not found: it MAY have been processed by another collector",
                        remote_path,
                    )
                    return

                # Permission problems
                self.logger.error(
                    "Cannot rename %s to %s",
                    remote_path,
                    processed_path,
                )
                raise

            self._current_remote = processed_path

            dest_path = os.path.join(self.args.working_directory, basename)

            self.download(processed_path, dest_path)

            if meta_path:
                meta_dest_path = os.path.join(
                    self.args.working_directory, os.path.basename(meta_path)
                )
                self.download(meta_path, meta_dest_path)

            # ingest the parent file using FileCollector
            super().ingest(dest_path, configs, force_update, report_folder=dirname)

        # catch broad exception to not break the file processing loop
        # pylint: disable=W0703
        except Exception as error:
            self.logger.error("Cannot ingest %s", remote_path)
            self.logger.exception(error)

    def get_remote_file_list(self, path: str):
        """
        build a list of remote file path

        Args:
            path (str):relative path to sftp_config.inbox_root

        TODO refactor as a generator that will refresh when exhausted
            and prioritize the entries with heapq based on timestamp present
            in file names
        """
        # add inbox_root as prefix of relative path
        path = os.path.join(self.sftp_config.inbox_root, path)

        remote_files = []

        self._healthcheck.tick()

        if self.sftp.isdir(path):
            for file_attr in self.sftp.listdir_attr(path):
                self._healthcheck.tick()
                if (
                    file_attr.filename.startswith(self.sftp_config.process_prefix)
                    and time.time() - file_attr.st_atime > self.sftp_config.age_limit
                ):
                    # handle obsolete file
                    self.logger.warning("Found too old file: %s", file_attr.filename)

                    forced_path = self.handle_too_old_file(path, file_attr.filename)

                    if forced_path:
                        remote_files.append(forced_path)

                elif file_attr.filename.startswith("."):
                    # skip hidden files
                    continue

                else:
                    remote_files.append(os.path.join(path, file_attr.filename))

        elif self.sftp.isfile(path):
            # warning: does not handle obsolete files
            remote_files.append(path)

        else:
            # won't handle symlink
            raise ValueError(f"Not a file or a directory: {path}")

        self.logger.debug("Files to process: %s", remote_files)

        return remote_files

    def get_ingested_dir(self) -> str:
        """get the directory where to put an ingested file

        Returns:
            [str]: directory path
        """
        return os.path.join(
            self.sftp_config.ingested_dir,
            self.get_relative_dir(),
            self.get_date_dirname(),
        )

    def get_rejected_dir(self) -> str:
        """get the directory where to put a rejected file

        Returns:
            str: directory path
        """
        return os.path.join(
            self.sftp_config.rejected_dir,
            self.get_relative_dir(),
            self.get_date_dirname(),
        )

    def on_ingest_error(self, path: str, config, error):
        """Override"""
        rejected_dir = self.get_rejected_dir()

        if not rejected_dir in self.__created_dirs:
            self.sftp.makedirs(rejected_dir)
            self.__created_dirs.add(rejected_dir)

        rejected_path = os.path.join(rejected_dir, os.path.basename(path))

        if self.sftp.isfile(rejected_path):
            self.logger.warning("Error log %s already exists: overwrite", rejected_path)
            self.sftp.remove(rejected_path)

        self.sftp.rename(self._current_remote, rejected_path)

        self.logger.info("Rejected file moved to  %s", rejected_path)

    def get_relative_dir(self) -> str:
        """get the relative path to the inbox of the current entry"""
        return os.path.relpath(
            os.path.dirname(self._current_remote), self.sftp_config.inbox_root
        )

    def on_ingest_finish(self, path, errors):
        """Override"""
        super().on_ingest_finish(path, errors)

        meta_path = (
            IngestionMeta.get_meta_path(path)
            if IngestionMeta.has_meta_file(path)
            else ""
        )

        # extract the relative path, i.e. remove the inbox prefix
        if errors:
            rejected_dir = self.get_rejected_dir()

            # don't create rejected_dir as it has been done by on_ingest_error()

            remote_error_log = os.path.join(
                rejected_dir, os.path.basename(self.error_log)
            )
            self.logger.info("Uploading error report to %s", remote_error_log)

            self.sftp.put(self.error_log, remote_error_log)

        else:
            ingested_dir = self.get_ingested_dir()

            if not ingested_dir in self.__created_dirs:
                self.sftp.makedirs(ingested_dir)
                self.__created_dirs.add(ingested_dir)

            ingested_path = os.path.join(ingested_dir, os.path.basename(path))

            self.logger.debug(
                "Planning file move %s to %s", self._current_remote, ingested_path
            )

            # post-pone file moves
            self.__files_to_move_args.append((self._current_remote, ingested_path))

            if meta_path:
                self.__files_to_move_args.append(
                    (
                        os.path.join(
                            os.path.dirname(self._current_remote),
                            os.path.basename(meta_path),
                        ),
                        os.path.join(ingested_dir, os.path.basename(meta_path)),
                    )
                )

        # remove local file in working directory
        self.logger.debug("Deleting local SFTP download: %s", path)

        os.remove(path)

        if meta_path:
            self.logger.debug("Deleting local SFTP meta download: %s", meta_path)
            os.remove(meta_path)

        # if loop took more time than age limit, flush message so files can be moved
        # FIXME this is not perfect at all: if a file ingestion take much time,
        # a concurent collector could decide to re-ingest the files that have not been
        # moved. So limit shall be considered with a factor or a ceil
        if (
            not self.should_stop_loop
            and time.time() - self.loop_start_time
            >= self.sftp_config.age_limit * self.CLEAN_UP_AGE_FACTOR
        ):
            self._flush_message_groups()

            # reset loop start time. this may causes excessive sleep time in loop, but
            # the compromise is rather good when watching every minute
            self.loop_start_time = time.time()

    def _flush_message_groups(self):
        """override: only move files after all messages have been sent"""
        super()._flush_message_groups()

        try:
            self.process_file_moves()
        except (FileNotFoundError, OSError, IOError) as exception:
            self.logger.critical("Cannot move files: %s", self.__files_to_move_args)
            self.logger.exception(exception)

    def process_file_moves(self):
        """move all the processed files"""
        while self.__files_to_move_args:
            source_path, target_path = self.__files_to_move_args.pop(0)

            try:
                if self.sftp.isfile(target_path):
                    self.logger.warning("%s already exists: overwrite", target_path)

                    self.sftp.remove(target_path)

                self.sftp.rename(source_path, target_path)

                self.logger.info(
                    "Successfully renamed %s to %s", source_path, target_path
                )
            except FileNotFoundError:
                # border case happens
                self.logger.error(
                    "Can't rename %s to %s",
                    source_path,
                    target_path,
                )
                self.logger.error(
                    "This could mean it has been considered too old "
                    "and re-ingested by another collector"
                )

    def handle_too_old_file(self, directory: str, filename: str) -> str:
        """Try to rename too old processing file so it can be ingested again in force
        update mode.

        Args:
            directory (str): directory on sftp server
            filename (str): file name

        Returns:
            str: renamed path if successfully, None if not
        """
        remote_path = os.path.join(directory, filename)

        target_path = os.path.join(directory, self.get_forced_filename(filename))

        try:
            self.logger.debug("Trying renaming %s to %s", remote_path, target_path)

            self.sftp.rename(remote_path, target_path)

            self.logger.info("Successfully renamed %s to %s", remote_path, target_path)

        except (FileNotFoundError, OSError, IOError):
            if not self.sftp.isfile(remote_path):
                self.logger.warning(
                    "%s not found: it MAY have been processed by another collector",
                    remote_path,
                )
                return None

            # Permission problems
            self.logger.error(
                "Cannot rename %s to %s",
                remote_path,
                target_path,
            )
            return None

        return target_path

    def get_processing_filename(self, filename: str) -> str:
        """return a unique processing filename for processing

        Args:
            filename ([str]): file name

        Returns:
            str: uniquely prefixed filename
        """
        return f"{self.sftp_config.process_prefix}{uuid.uuid4().hex}-{filename}"

    def get_forced_filename(self, processing_name: str) -> str:
        """return a file name usable for force update from a processing file name

        Args:
            processing_name (str): processing prefixed filename

        Returns:
            str: suffixed filename
        """
        return processing_name[self.__prefix_length :] + self.sftp_config.force_suffix

    def download(self, remote_path: str, local_path: str):
        """Download remote file and log network speed

        Args:
            remote_path ([str]): file path on sftp
            local_path ([str]): file path on local storage
        """

        self.logger.debug("Downloading %s to %s ", remote_path, local_path)

        start_time = time.time()

        self.sftp.get(remote_path, local_path)

        dowload_duration = time.time() - start_time

        size = os.path.getsize(local_path)

        self.logger.info(
            "Downloaded %s %d bytes in %f seconds at %.2fKB/s",
            remote_path,
            size,
            dowload_duration,
            size / 1024 / dowload_duration,
        )

    @classmethod
    def attributs_url(cls):
        return super().attributs_url() + ["hostname"]

    @classmethod
    def document(cls, config: SFTPConfiguration):
        information = super().document(config)
        information |= {
            "protocol": "SFTP",
            "auth_user": getattr(config, "client_username"),
        }
        return information
