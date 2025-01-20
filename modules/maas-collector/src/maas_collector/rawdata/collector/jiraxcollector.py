"""Extract files from JIRA rest API"""

import base64
import datetime
import json
import os
import pathlib
from dataclasses import dataclass, field
from typing import Any, Dict

import dateutil.parser
import jira
import jira.resources
from maas_collector.rawdata.collector.filecollector import (
    FileCollector,
    FileCollectorConfiguration,
)
from maas_collector.rawdata.collector.journal import (
    CollectingInProgressError,
    CollectorJournal,
    NoRefreshException,
)


# Désactive la génération automatique de __repr__ pour pouvoir utiliser
# celui du parent qui masque les données sensible comme les mot de passe
@dataclass(repr=False)
class JiraExtendedCollectorConfiguration(FileCollectorConfiguration):
    """Configuration for Jira collection"""

    end_point: str = ""

    jql_query: str = ""

    auth_method: str = ""

    username: str = ""

    password: str = field(default="", metadata={"sensitive": True})

    token: str = field(default="", metadata={"sensitive": True})

    proxy_login: str = ""

    proxy_password: str = field(default="", metadata={"sensitive": True})

    ingest_attachements: bool = False

    attachement_prefix: bool = False

    refresh_interval: int = 0

    expand = "changelog"

    timeout = 120

    @property
    def has_proxy_auth(self) -> bool:
        """tell if proxy credentials are present

        Returns:
            bool: true if proxy credentials are present
        """
        return bool(self.proxy_login and self.proxy_password)


class JIRAExtendedCollector(FileCollector):
    """A collector that collect from a JIRA REST api.

    Could be one day refactored to more generic REST api collector.

    Warning: does not support redirect
    """

    CONFIG_CLASS = JiraExtendedCollectorConfiguration

    def ingest(self, path=None, configs=None, force_update=None):
        """Ingest from JIRA. All arguments are ignored so defaults to None"""
        # iterate over all JIRA collector configurations
        for config in self.configs:
            if not config.end_point:
                # skip configuration with no end_point like configuration for
                # attachement ingestion
                continue

            try:
                # use the journal as context to secure the concurent collect and keep
                # the last update date
                with CollectorJournal(config) as journal:
                    self._healthcheck.tick()

                    self.ingest_tickets(config, journal)

            except CollectingInProgressError:
                # Errors should never pass silently.
                self.logger.info(
                    "On going collection on interface %s: skipping",
                    config.interface_name,
                )
            except NoRefreshException:
                self.logger.info(
                    "Interface %s does not need to be refreshed: skipped",
                    config.interface_name,
                )
            finally:
                # flush messages between interfaces as they don't ingest the same data
                self._flush_message_groups()

            if self.should_stop_loop:
                break

    @classmethod
    def build_client(cls, config: JiraExtendedCollectorConfiguration) -> jira.JIRA:
        """Create a Jira instance

        Args:
            config (JiraExtendedCollectorConfiguration): configuration

        Returns:
            jira.JIRA: initialized Jira client instance
        """
        # arguments for JIRA constructor
        argv: Dict[str, Any] = {}

        match config.auth_method:
            case "basic":
                argv["basic_auth"] = (config.username, config.password)

            case "cookie_based":
                # this is deprecated but used by some subcontractors
                argv["auth"] = (config.username, config.password)

            case "token_based":
                argv["token_auth"] = config.token

            case "jira_cloud":
                # JIRA cloud special case: basic auth with token as password
                # https://jira.readthedocs.io/examples.html#jira-cloud
                argv["basic_auth"] = (config.username, config.token)

            case _:
                raise ValueError(f"Unsupported auth method: '{config.auth_method}'")

        if config.has_proxy_auth:
            # add http "proxy" authorization (EDRS case) that add basic authentication
            # to the Authorization header
            argv["options"] = {
                "headers": {
                    "Authorization": "Basic "
                    + base64.b64encode(
                        b":".join(
                            (
                                config.proxy_login.encode(),
                                config.proxy_password.encode(),
                            )
                        )
                    )
                    .strip()
                    .decode()
                }
            }

        return jira.JIRA(
            config.end_point, timeout=(config.timeout, config.timeout), **argv
        )

    def ingest_tickets(
        self, config: JiraExtendedCollectorConfiguration, journal: CollectorJournal
    ):
        """Ingest tickets

        Args:
            config (JiraCollectorConfiguration): configuration to ingest
        """
        client = self.build_client(config)

        # TODO handle start/stop for replay
        if journal.last_date:
            date_criteria = f'"{journal.last_date.strftime("%Y-%m-%d %H:%M")}"'
        else:
            date_criteria = "-30d"

        jql_str = config.jql_query.format(date_criteria=date_criteria)

        self.logger.info("Querying %s with request: %s", config.interface_name, jql_str)

        start_at = total = 0

        filename_prefix = "_".join(
            (
                config.interface_name,
                datetime.datetime.utcnow().strftime(
                    "%Y%m%d_%H%M%S%f"
                ),  # UUID could be better
            )
        )

        try:
            while start_at == 0 or start_at < total:
                if self.should_stop_loop:
                    break

                self._healthcheck.tick()

                # a pseudo full payload to store raw issue json for later ingestion
                # by json extractor (for backward compatibility and replay)
                payload_dict = {"issues": []}

                issues_attachments = []

                last_date = None

                issues = client.search_issues(jql_str, startAt=start_at)

                if issues.total == 0:
                    self.logger.info("%s returned no new issue", jql_str)
                    break

                if total == 0:
                    self.logger.info(
                        "%s returned a total of %s issues", jql_str, issues.total
                    )
                    total = issues.total
                elif total != issues.total:
                    # prevent infinite loop when a ticket is deleted
                    self.logger.warning(
                        "total number of tickets changed during ingestion loop "
                        "from %s to %s. "
                        "Remaining tickets will be ingested at next loop.",
                        total,
                        issues.total,
                    )
                    break

                # iterate other issues to populate tickets and attachements
                for issue in issues:
                    self._healthcheck.tick()

                    issue_date = dateutil.parser.parse(issue.fields.updated)
                    # JQL does not support seconds in its date format
                    # 10 years people want it
                    # https://jira.atlassian.com/browse/JRASERVER-31250
                    # so additionnal check is required with the real issue date

                    if journal.last_date and not issue_date > journal.last_date:
                        self.logger.debug(
                            "Skipping %s: too old (%s)", issue, issue.fields.updated
                        )
                        continue

                    if config.extractor:
                        # conventional ticket ingestion if performed with JSON extractor
                        # for backward compatibility
                        payload_dict["issues"].append(issue.raw)

                    if config.ingest_attachements and issue.fields.attachment:
                        self.logger.debug(
                            "Attachment found: %s", issue.fields.attachment
                        )
                        # ingest attachements
                        issues_attachments.append((issue, issue.fields.attachment))

                    last_date = issue_date

                # ingest tickets
                if payload_dict["issues"]:
                    page_id = int(round(start_at / len(issues))) + 1

                    filename = os.path.join(
                        self.args.working_directory,
                        f"{filename_prefix}_{page_id}.json",
                    )

                    self._healthcheck.tick()

                    self.ingest_issues_payload(config, payload_dict, filename)

                # ingest attachments
                for issue, attachments in issues_attachments:
                    if config.attachement_prefix:
                        prefix = f"{issue.key}_"

                    else:
                        prefix = ""

                    for attachment in attachments:
                        self._healthcheck.tick()
                        self.ingest_attachement(attachment, prefix)

                # save only at the end of the page cause of compatibility with
                # json extractor
                if last_date:
                    journal.last_date = last_date

                journal.tick()

                start_at += len(issues)
        finally:
            # clean http session
            client.close()

    def ingest_issues_payload(
        self,
        config: JiraExtendedCollectorConfiguration,
        payload_dict: dict,
        filename: str,
    ):
        """ingest a json payload of a search result

        Args:
            config (JiraExtendedCollectorConfiguration): configuration
            payload_dict (dict): data dictionnary
            filename (str): path to save the payload
        """
        with open(filename, "w", encoding="utf-8") as payload_fd:
            json.dump(payload_dict, payload_fd)

        try:
            self.extract_from_file(
                filename,
                config,
                force_update=self.args.force,
                report_name=pathlib.Path(filename).name,
            )
        # catch broad exception to not break the loop
        # pylint: disable=W0703
        except Exception as error:
            self.logger.error("Error ingesting %s: %s", filename, error)
        # pylint: enable=W0703
        finally:
            os.remove(filename)

    def ingest_attachement(
        self, attachment: jira.resources.Attachment, prefix: str = ""
    ):
        """Ingest a attached file

        Args:
            attachment (jira.resources.Attachment): attachment object
        """

        configurations = self.get_configurations(attachment.filename)

        if not configurations:
            # does not match
            self.logger.debug(
                "%s does not match any file pattern: skipped", attachment.filename
            )
            return

        download_path = os.path.join(
            self.args.working_directory, prefix + attachment.filename
        )

        self.logger.info(
            "Downloading attachement %s to %s", attachment.id, download_path
        )

        with open(download_path, "wb") as attacement_fd:
            attacement_fd.write(attachment.get())

        try:
            for configuration in configurations:
                try:
                    self.extract_from_file(
                        download_path,
                        configuration,
                        force_update=self.args.force,
                        report_name=os.path.basename(download_path),
                    )
                # catch broad exception to not break the loop
                # pylint: disable=W0703
                except Exception as error:
                    self.logger.error(
                        "Error ingesting attachement %s: %s", attachment, error
                    )
        finally:
            self.logger.debug("Deleting %s", download_path)
            os.remove(download_path)

    @classmethod
    def probe(cls, config: JiraExtendedCollectorConfiguration, probe_data):
        # test connection by building client
        try:
            client = cls.build_client(config)
            config.status = "OK"
            client.close()

        except (jira.JIRAError, ConnectionError) as error:
            config.status = "KO"
            raise error

    @classmethod
    def attributs_url(cls):
        return super().attributs_url() + ["end_point"]

    @classmethod
    def document(cls, config: JiraExtendedCollectorConfiguration):
        information = super().document(config)

        auth_method = getattr(config, "auth_method", "No auth")
        if config.has_proxy_auth:
            auth_method += f" - with proxy {config.proxy_login}"
        information |= {
            "protocol": "HTTP(S)",
            "auth_method": auth_method,
            "auth_user": getattr(config, "username"),
        }
        return information
