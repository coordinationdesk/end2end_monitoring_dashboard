"""

Contains CredentialMixin class that add capability to load a json configuration file
for credential storage and populate interface configuration with credential info.
"""

import json
import logging
import os

# as CredentialMixin provides only a specific function, it is not expected to contain
# lot of methods
# pylint: disable=R0903

LOGGER = logging.getLogger("CredentialMixin")


class CredentialMixin:
    """

    Mixin class to provide credential file loading for collectors who need it
    """

    @staticmethod
    def load_credential_dict(credential_file: str) -> dict:
        """
        Read a credential file and build a dict with interface names as key and
        the remaining dict as value

        Args:
            credential_file (str): path

        Returns:
            dict: populated dict
        """
        # consistency checks
        if not credential_file:
            raise ValueError("No Credential file specified")

        if not os.path.isfile(credential_file):
            raise FileNotFoundError(
                f"Credential file {credential_file} does not exists"
            )

        credential_dict = {}

        with open(credential_file, encoding="UTF-8") as credential_fd:

            credential_json = json.load(credential_fd)

            for interface in credential_json["interfaces"]:
                credential_dict[interface["name"]] = interface
                del interface["name"]

        return credential_dict

    @staticmethod
    def set_credential_attributes(config, credential_dict: dict):
        """set configuration attributes with data extracted from credential dict

        Args:
            config: configuration
            credential_dict (dict): credential dictionnary

        Raises:
            KeyError: if no credentials are found
        """

        if (
            config.interface_credentials not in credential_dict
            and config.interface_name not in credential_dict
        ):
            LOGGER.warning(
                "No credential configuration found for interface %s",
                config.interface_name,
            )
            return

        if_dict = {
            **credential_dict.get(config.interface_credentials, {}),
            **credential_dict.get(config.interface_name, {}),
        }

        for name, value in if_dict.items():
            if not hasattr(config, name):
                LOGGER.warning(
                    "%s %s has not attribute %s",
                    config.__class__.__name__,
                    config.interface_name,
                    name,
                )
            setattr(config, name, value)

    def load_credentials(self, credential_file: str):
        """load credential file and populate configurations with username, password ...

        Args:
            credential_file (str): path to the credential file

        Raises:
            FileNotFoundError: if credential_file is not found
            ValueError: if credential_file is empty

        """

        credential_dict = self.load_credential_dict(credential_file)

        # iterate over all configuration and populate credentials from file data
        for config in self.configs:

            self.set_credential_attributes(config, credential_dict)


# pylint: enable=R0903
