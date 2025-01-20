import sys
from maas_collector.rawdata.cli.lib.args import get_collector_args
from maas_collector.rawdata.collector.credentialmixin import CredentialMixin
from maas_collector.rawdata.collector.filecollector import CollectorArgs, FileCollector
from maas_collector.rawdata.collector.monitorcollector import InterfaceMeta
from maas_collector.rawdata.configuration import (
    load_json as load_configuration_json,
    find_configurations,
)

from maas_collector.rawdata.implementation import (
    get_collector_class_by_config_classname,
)
import json
import maas_collector.rawdata.cli.lib.log as maas_log
from maas_collector.rawdata.cli.lib.args import (
    common_parser,
    get_collector_args,
    EnvDefault,
)


class CollectorInterfaceGenerator(FileCollector):
    def setup(self):
        credential_dict = self.load_credential_dict(self.args.credential_file)
        nb_interface_inside_dict = len(credential_dict.keys())

        interfaces_documentation = []

        # load the configurations of the interfaces to monitor
        for config_path in find_configurations(self.args.rawdata_config_dir):
            print(config_path)
            with open(config_path, mode="r", encoding="UTF-8") as conf_obj:
                conf_dict = json.load(conf_obj)

            self.logger.debug("Looking in %s", config_path)

            for collect_conf_dict in conf_dict.get("collectors", []):
                if not collect_conf_dict.get("class"):
                    self.logger.info(
                        "Class property empty. Ignoring some configuration in %s",
                        config_path,
                    )
                    continue

                if (
                    collect_conf_dict["class"]
                    == "InterfaceMonitorCollectorConfiguration"
                ):
                    self.logger.debug(
                        "Ignoring InterfaceMonitorConfiguration: %s", config_path
                    )
                    continue

                collector_class = get_collector_class_by_config_classname(
                    collect_conf_dict["class"]
                )

                config = [
                    config
                    for config in load_configuration_json(
                        config_path, collector_class.CONFIG_CLASS
                    )
                    if config.interface_name == collect_conf_dict["interface_name"]
                ][0]

                self.logger.debug("Applying credentials to %s", config.interface_name)

                try:
                    self.set_credential_attributes(config, credential_dict)
                except KeyError as error:
                    self.logger.warning(error)
                    continue

                # meta_list.append(interface_meta)
                # print(config)
                documentation = collector_class.document(config)
                interfaces_documentation.append(documentation)

        print(interfaces_documentation)
        with open("data.json", "w") as outfile:
            json.dump(interfaces_documentation, outfile, indent=4, sort_keys=True)


def generate_interface_doc_main(args):
    parser = common_parser()

    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(CollectorArgs, namespace)

    instance = CollectorInterfaceGenerator(args)
    instance.setup()


if __name__ == "__main__":
    generate_interface_doc_main(sys.argv[1:])
