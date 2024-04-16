"""Base classes and function for migrations"""
import argparse
from datetime import datetime
import fnmatch
import json
import lzma
import logging
import os
import sys

import opensearchpy.connection.connections as db_connections
from opensearchpy.helpers import parallel_bulk
from opensearchpy.exceptions import NotFoundError, RequestError

from maas_engine.cli import args as maas_args
from maas_engine.cli.log import setup_logging


# *search indices methods like put_template have arguments handled by decorator
# and are not present in the final signature, so 'unexpected-keyword-arg' rule
# is disabled
# pylint: disable=E1123
class MaasMigrator:
    """Base class for migrations"""

    TEMP_INDEX_PREFIX = "migration"

    TEMPLATE_DIR = "templates"

    DATA_DIR = "data"

    def __init__(self, args):
        """constructor

        Args:
            args (namespace): parsed cli arguments
        """
        self.args = args
        self.es_conn = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.index_names = []
        self.available_templates = []

    def setup(self):
        """setup connections"""

        if self.args.dry_run:
            self.logger.warning(
                "Dry mode is on: not modification will happen on existing data"
            )

        # get the list of available templates following maas suffix convention
        self.available_templates = [
            name[:-14]
            for name in fnmatch.filter(
                os.listdir(os.path.join(self.args.resources, self.TEMPLATE_DIR)),
                "*_template.json",
            )
        ]
        self.available_templates.sort()
        self.logger.info(
            "Found %d local templates in %s",
            len(self.available_templates),
            self.args.resources,
        )

        # connect to database
        es_url = maas_args.get_es_credentials_url(self.args)

        self.logger.info("Setup connection to opensearch: %s", es_url)

        self.es_conn = db_connections.create_connection(
            hosts=[es_url],
            retry_on_timeout=True,
            max_retries=self.args.es_retries,
            timeout=self.args.es_timeout,
            verify_certs=not self.args.es_ignore_certs_verification,
            ssl_show_warn=not self.args.es_ignore_certs_verification,
        )

        self.logger.info(
            "Found %d remote indices", len(self.es_conn.indices.get_alias("*"))
        )

    @classmethod
    def migration_action_iterator(cls, func):
        """Decorator for action iterator to allow dry run

        Args:
            func (callable): a bulk action generator method
        """

        def wrapper(self):
            self.logger.info(func.__doc__)

            ignored_count = 0
            for action in func(self):
                if not self.args.dry_run:
                    yield action
                else:
                    ignored_count += 1
                    self.logger.debug("Ignoring %s", action)

            if self.args.dry_run or ignored_count > 0:
                self.logger.info("%d action ignored", ignored_count)

        return wrapper

    def bulk_exec(self, iterator):
        """Encapsulate bulk execution

        Args:
            iterator (generator): bulk action iterator
        """
        for success, info in parallel_bulk(
            db_connections.get_connection(),
            iterator,
            refresh=True,
            # raise_on_error=False,
            # raise_on_exception=False,
            request_timeout=self.args.es_timeout,
        ):
            if not success:
                self.logger.error(info)
            else:
                self.logger.debug(info)

    def load_template(self, index_name: str) -> dict:
        """load a template

        Args:
            index_name (str): index name

        Returns:
            dict: template loaded from json
        """
        template_path = os.path.join(
            self.args.resources, self.TEMPLATE_DIR, f"{index_name}_template.json"
        )

        self.logger.info("Reading template %s", template_path)

        with open(template_path, encoding="utf-8") as template_fd:
            template_data = json.load(template_fd)

        return template_data

    def populate_index(self, filename: str) -> dict:
        """load a bulk file

        Args:
            file_name (str): Name of file to be read.
                             Must be in bulk format:
                             {"_op_type": "index","_index":"index-name","_source": {"name": "blabla"}}
        Returns:
            Nothing
        """
        bulk_path = os.path.join(self.args.resources, self.DATA_DIR, filename)

        self.logger.info("Reading bulk %s", bulk_path)

        def read_content():
            with lzma.open(bulk_path, "rt") as data_fd:
                for line in data_fd:
                    update = json.loads(line)
                    yield update

        self.bulk_exec(read_content())
        self.logger.info("Update sent")

    def get_index_list(self, index_name_prefix, partitions=None) -> list:
        """get the list of indices starting by a string prefix

        Args:
            index_name (str): prefix string

        Returns:
            list: list of index names
        """
        indices = self.es_conn.indices.get_alias(f"{index_name_prefix}-*")
        name_list = list(indices.keys())
        name_list.sort()

        if partitions:
            tmp_list = []
            for name in name_list:
                for partition_suffix in partitions:
                    if name.endswith(f"-{partition_suffix}"):
                        tmp_list.append(name)
            name_list = tmp_list
        return name_list

    def migrate_index_template(self, index_name, partitions, script=None):
        """Migrate the template of an index by reindexing it into a temporary new one
        then reindexing it back to the original name. Useful when field type changing

        Args:
            index_name (str): name of the index
        """
        empty_indices = []

        template_data = self.load_template(index_name)

        name_list = self.get_index_list(index_name, partitions)

        self.logger.info("Found %d indices to migrate: %s", len(name_list), name_list)

        # configure the temporary template by adding prefix to alias and pattern
        temp_template_data = self.load_template(index_name)

        temp_template_data["index_patterns"][
            0
        ] = f"migrating-{temp_template_data['index_patterns'][0]}"

        temp_template_data["aliases"] = {
            f"migrating-{key}": value
            for key, value in temp_template_data["aliases"].items()
        }

        # create the temporary template
        self.es_conn.indices.put_template(
            f"template_migrating-{index_name}",
            temp_template_data,
            request_timeout=self.args.es_timeout,
        )

        # step 1: reindex to temporary indices with new template
        # if anything breaks, original data are still safe
        for name in name_list:
            self.logger.info("Migrating %s", name)

            temp_name = f"migrating-{name}"

            if self.es_conn.indices.exists(temp_name):
                self.logger.warning("Temporary index %s already exists", temp_name)

            self.logger.info("Reindexing documents from %s to %s", name, temp_name)

            reindex_payload = {
                "source": {"index": name},
                "dest": {"index": temp_name},
            }

            if script is not None:
                reindex_payload["script"] = script

            result = self.es_conn.reindex(
                reindex_payload,
                refresh=True,
                request_timeout=self.args.es_timeout,
            )

            self.logger.info(result)

            if result["total"] == 0:
                empty_indices.append(name)

        # step 2: reindex to final indices as temporary indices have been filled
        # correctly

        # update the target template
        self.es_conn.indices.put_template(
            f"template_{index_name}",
            template_data,
            request_timeout=self.args.es_timeout,
        )

        for name in name_list:
            if name in empty_indices:
                continue

            temp_name = f"migrating-{name}"

            if self.args.dry_run:
                continue

            self.logger.info("Deleting %s", name)
            self.es_conn.indices.delete(name, request_timeout=self.args.es_timeout)

            self.logger.info(
                "Reindexing documents from %s to %s",
                temp_name,
                name,
            )

            result = self.es_conn.reindex(
                {"source": {"index": temp_name}, "dest": {"index": name}},
                refresh=True,
                request_timeout=self.args.es_timeout,
            )

            self.logger.info(result)

            self.logger.info("Deleting temporary index %s", temp_name)
            self.es_conn.indices.delete(temp_name, request_timeout=self.args.es_timeout)

        # clean up templates
        self.es_conn.indices.delete_template(f"template_migrating-{index_name}")

    def update_index(self, index_name):
        """update index template and mapping for all indices matching index_name

        Args:
            index_name (str): index name
        """
        template_data = self.load_template(index_name)

        for name in self.get_index_list(index_name):
            self.logger.info("Put new mapping to %s", index_name)

            if self.args.dry_run:
                continue

            self.es_conn.indices.put_mapping(
                body=template_data["mappings"],
                index=name,
                request_timeout=self.args.es_timeout,
            )

        self.logger.info("Put new template to template_%s", index_name)

        if self.args.dry_run:
            return

        # update the target template
        self.es_conn.indices.put_template(
            f"template_{index_name}",
            template_data,
            request_timeout=self.args.es_timeout,
        )

    def install_index(self, index_name):
        """put template of the index

        Args:
            index_name (str): index name
        """
        self.logger.info("Installing %s template", index_name)
        template_data = self.load_template(index_name)

        if not self.args.dry_run:
            self.es_conn.indices.put_template(f"template_{index_name}", template_data)

            if not self.es_conn.indices.exists(index_name):
                self.logger.info("%s does not exist: creating index", index_name)
                self.create_index(index_name)
            else:
                self.logger.info("%s exists: try PUT mapping on existing", index_name)
                try:
                    self.update_index(index_name)
                except RequestError as error:
                    self.logger.error("Cannot update mapping %s: %s", index_name, error)
                    self.logger.error("%s may require migration.", index_name)

    def delete_index_related(self, index_names):
        """Delete indices and templates related to the index names

        Note: index without '-' will not be deleted

        Args:
            index_names (list[str]): list of index/template that need to be deleted
                                    if "all" this deleted all indices and templates
        """

        # all option
        if "all" in index_names:
            # templates
            self.logger.info("Delete all template")

            if not self.args.dry_run:
                self.es_conn.indices.delete_template("*")
                self.logger.info("Delete all templates")

            # indices
            self.logger.info("Delete all indices")

            if not self.args.dry_run:
                # NOTE: to delete with '*' we need specific permission not provided by default
                self.es_conn.indices.delete("*-*")
                self.logger.info("Delete all indices")

            return

        # index list
        for index_name in index_names:
            # template
            self.logger.info("Delete template %s", index_name)

            if not self.args.dry_run:
                try:
                    self.es_conn.indices.delete_template(f"template_{index_name}")
                    self.logger.info("Delete %s template", index_name)
                except NotFoundError:
                    self.logger.info("%s template not exist", index_name)

            # indices
            self.logger.info("Delete %s indices", index_name)

            if not self.args.dry_run:
                self.es_conn.indices.delete(f"{index_name}*")
                self.logger.info("Delete %s indices", index_name)

    def create_index(self, index_alias):
        """Create a index with the template partition format

        Note: The index must have a template available

        Args:
            index_alias (str): index_name use for extract template partition format
        """
        try:
            template_data = self.load_template(index_alias)

            partition_format = template_data["mappings"]["_meta"]["partition_format"]
            extension = datetime.now().strftime(partition_format)
            index_name = f"{index_alias}-{extension}"

            self.logger.info("Create index %s", index_name)
            if self.args.dry_run:
                return
            self.es_conn.indices.create(index_name)
        except KeyError as error:
            self.logger.warning("Can't create index, template missing: %s", error)

    def get_effective_template_list(
        self, template_list: list[str], allow_missing=False
    ) -> list[str]:
        """get the list of template validating their presence

        Args:
            template_list (list[str]): list of name. 'all' will return all available
            allow_missing (bool): don't raise exception if a template is missing

        Raises:
            RuntimeError: if any argument template is not found

        Returns:
            list[str]: list of available template name
        """

        if template_list == ["all"]:
            return self.available_templates

        missing = [
            index_name
            for index_name in template_list
            if index_name not in self.available_templates
        ]

        if missing and not allow_missing:
            raise RuntimeError(f"Missing templates: {' '.join(missing)}")

        return set(template_list) - set(missing)

    def run(self):
        """Template method: perform the migration statements"""


def migration_main(argv, migrator_class):
    """Entry point for migrator subclass execution

    Args:
        argv (list): arguments
        migrator_class (class): Migrator subclass
    """

    parser = argparse.ArgumentParser(
        parents=[
            maas_args.log_parser(),
            maas_args.es_parser(),
        ]  # , maas_args.amqp_parser()]
    )
    parser.add_argument(
        "-d", "--dry-run", action="store_true", help="Don't modify database"
    )

    # resources directory
    parser.add_argument(
        "-r", "--resources", default="/app/resources", help="resources directory"
    )

    parser.add_argument(
        "-i",
        "--install",
        help="Install one or more index template (put). ('all' for all templates)",
        nargs="+",
    )

    parser.add_argument(
        "-l", "--list", action="store_true", help="list available templates"
    )

    parser.add_argument(
        "-m",
        "--migrate",
        help="Migrate one or more index template (put) and reindex. ('all' for all templates)",
        nargs="+",
    )

    parser.add_argument(
        "-p",
        "--partition",
        help="migrate only a set of partitions",
        nargs="+",
    )

    parser.add_argument(
        "--populate",
        help="put bulk data into ES (can be xz-compressed)",
        nargs="+",
    )

    parser.add_argument(
        "--script",
        help="script to use during index migrating",
    )

    parser.add_argument(
        "--nuke",
        help="💣 nuke the database : delete indexes, reinstall templates, "
        "create indexes (use all for all indexes)",
        nargs="+",
    )

    args = parser.parse_args(argv)

    if not os.path.isdir(args.resources):
        sys.stderr.write(f"Resource directory not found: {args.resources}{os.linesep}")
        sys.stderr.write(f"Use -r or --resources to specify it{os.linesep}")
        sys.exit(1)

    setup_logging(args.loglevel)

    logging.info(migrator_class.__doc__)

    migrator = migrator_class(args)

    migrator.setup()

    if args.list:
        for template in migrator.available_templates:
            partition_names = " ".join(
                [
                    name[len(template) + 1 :]
                    for name in migrator.get_index_list(template)
                ]
            )
            print(template, ":", partition_names)
        sys.exit()

    if args.install:
        for index_name in migrator.get_effective_template_list(args.install):
            migrator.install_index(index_name)

    if args.migrate:
        for index_name in migrator.get_effective_template_list(args.migrate):
            script = json.loads(args.script) if args.script else None
            migrator.migrate_index_template(index_name, args.partition, script)

    if args.nuke:
        migrator.delete_index_related(args.nuke)
        for index_name in migrator.get_effective_template_list(
            args.nuke, allow_missing=True
        ):
            migrator.install_index(index_name)

    if args.populate:
        for filename in args.populate:
            migrator.populate_index(filename)

    # no command line action: run the custom migration code
    if not (args.install or args.migrate):
        migrator.run()


def run():
    """entry point for pyscaffold"""
    migration_main(sys.argv[1:], MaasMigrator)


if __name__ == "__main__":
    run()
