"""Module used for HTTP OAuth authentification operation"""

import base64
import datetime
import logging

from dataclasses import dataclass
from requests import RequestException

# pylint: disable=line-too-long / C0301


@dataclass
class BasicConfiguration:
    """Configuration for Authentication"""

    client_username: str = ""

    client_password: str = ""

    token_field_header: str = ""


@dataclass
class OAuthConfiguration:
    """Oauth Configuration"""

    client_username: str = ""

    client_password: str = ""

    oauth_basic_credential: str = ""

    token_field_header: str = ""

    token_url: str = ""

    client_id: str = ""

    client_secret: str = ""

    scope: str = None

    grant_type: str = "password"

    auth_timeout: int = 120


class Authentication:
    """Default authentication workflow"""

    # @classmethod
    # def __init_subclass__(cls, **kwargs):
    #     super().__init_subclass__(**kwargs)

    def __init__(self, config, http_session) -> None:
        self.token_field_header = config.token_field_header
        self.token = config.token
        self.http_session = http_session
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_token(self):
        """Return the current token

        Returns:
            str: the current token
        """

        return self.token

    def get_headers(self):
        """Return the headers with the token

        Returns:
            dict: The header formatted with the token
        """

        if self.token_field_header:
            return {self.token_field_header: self.get_token()}
        return {}


class OAuth(Authentication):
    """OAuth authentication workflow"""

    def __init__(self, config: OAuthConfiguration, http_session) -> None:
        super().__init__(config, http_session)

        self.token_url = config.token_url
        self.basic_credential = config.oauth_basic_credential
        self.client_id = config.client_id
        self.client_secret = config.client_secret
        self.client_username = config.client_username
        self.client_password = config.client_password
        self.timeout = config.auth_timeout

        self.scope = config.scope
        self.grant_type = config.grant_type

        self.access_token_expiration_date = datetime.datetime.now()

        self.refresh_token_expiration_date = None
        self.refresh_token = None

    def get_token(self):
        now = datetime.datetime.now()
        if self.access_token_expiration_date <= now:
            # Without refresh
            if (
                self.refresh_token_expiration_date is None
                or self.refresh_token_expiration_date <= now
            ):
                self.logger.debug("Creating new token")
                self._init_token()
            else:
                self.logger.debug("Creating a new access token using refresh")
                self._refresh_token()

        return super().get_token()

    def _init_token(self):
        raw_data = f"grant_type={self.grant_type}&client_secret={self.client_secret}"

        if self.client_id:
            raw_data += f"&client_id={self.client_id}&"

        if not self.grant_type == "client_credentials":
            raw_data += (
                f"&username={self.client_username}&password={self.client_password}"
            )

        if self.scope is not None:
            raw_data += f"&scope={self.scope}"

        headers = {"Content-type": "application/x-www-form-urlencoded"}

        if self.basic_credential:
            headers["Authorization"] = f"Basic {self.basic_credential}"

        try:
            response = self.http_session.post(
                self.token_url,
                data=raw_data,
                headers=headers,
                timeout=self.timeout,
                verify=False,
            )
        except RequestException as connection_error:
            self.logger.error("[OAuth] - Failed to fetch token from %s", self.token_url)
            raise connection_error

        if not 200 <= response.status_code < 300:
            # serious problem
            self.logger.error(
                "Error querying token at %s %d: %s",
                self.token_url,
                response.status_code,
                response.content,
            )
            raise ValueError(f"Error querying token {self.token_url}")

        response_json = response.json()

        # Handle
        if response_json["token_type"].lower() == "bearer":
            self.token = f"Bearer {response_json['access_token']}"

        else:
            self.logger.warning("Unhandle scope : %s", response_json["token_type"])
            self.token = response_json["access_token"]

        now = datetime.datetime.now()

        # Handle refresh if got one
        if "refresh_token" in response_json:
            self.refresh_token = response_json["refresh_token"]

            if "refresh_expires_in" in response_json:
                refresh_validity = response_json["refresh_expires_in"]
                self.refresh_token_expiration_date = now + datetime.timedelta(
                    seconds=refresh_validity
                )
            else:
                self.refresh_token_expiration_date = None

        else:
            self.refresh_token = None

        # default access - 1d
        access_validity = response_json.get("expires_in", 86400)
        self.access_token_expiration_date = now + datetime.timedelta(
            seconds=access_validity
        )

    def _refresh_token(self):
        """Refresh the access token using the refresh

        Raises:
            ValueError: Failed to refresh to the token
        """

        raw_data = (
            "grant_type=refresh_token&"
            f"refresh_token={self.refresh_token}&"
            f"client_id={self.client_id}&"
            f"client_secret={self.client_secret}&"
        )

        if self.scope is not None:
            raw_data += f"&scope={self.scope}"

        headers = {"Content-type": "application/x-www-form-urlencoded"}
        now = datetime.datetime.now()

        try:
            response = self.http_session.post(
                self.token_url,
                data=raw_data,
                headers=headers,
                timeout=self.timeout,
            )
        except RequestException as connection_error:
            self.logger.error("[OAuth] - Failed to refresh token")
            raise connection_error

        if not 200 <= response.status_code < 300:
            # serious problem
            self.logger.error(
                "Error refreshing token at %s %d: %s",
                self.token_url,
                response.status_code,
                response.content,
            )
            raise ValueError(f"Error refreshing token {self.token_url}")

        response_json = response.json()

        if response_json["token_type"].lower() == "bearer":
            self.token = f"Bearer {response_json['access_token']}"

        else:
            self.token = response_json["access_token"]

        self.access_token_expiration_date = now + datetime.timedelta(
            seconds=response_json["expires_in"]
        )


class Basic(Authentication):
    """Basic authentication workflow"""

    def __init__(self, config: BasicConfiguration, http_session) -> None:
        super().__init__(config, http_session)

        self.token = self._generate_token(
            config.client_username, config.client_password
        )

    def _generate_token(self, username, password):
        """Encode the credentials to have the basic token

        Args:
            username (str): The username to use
            password (str): The password to use

        Returns:
            str: the formated token which encodes credentials
        """

        user_pass = f"{username}:{password}"

        b64_token = base64.b64encode(user_pass.encode()).decode()

        formated_token = f"Basic {b64_token}"

        return formated_token


class SessionAuth(Authentication):
    """
    Session-Based Authentication Workflow
    In this workflow, authentication is managed within the HTTP session itself.
    For example, after logging in through a login URL, the same HTTP session can be used to access protected data,
    with all authentication details remaining within the session.
    """

    def __init__(self, config: BasicConfiguration, http_session) -> None:
        super().__init__(config, http_session)
        self.login_url = config.login_url
        self.timeout = config.auth_timeout
        self._login(config.credentials)

    def _login(self, credentials):
        """
        Authenticates the client by sending the user's credentials to the server.

        Args:
            credentials (dict): A dictionary of the form
                {
                    "username_field": "username",
                    "password_field": "password"
                }
                where:
                - username_field (str): The expected form field name for the user's identifier.
                - password_field (str): The expected form field name for the user's password.
                - username (str): The user's identifier or username.
                - password (str): The user's password.

        Raises:
            connection_error: Raised when there is a connection issue with the authentication server.
            ValueError: Raised when required credentials are missing or improperly formatted.
        """

        try:
            response = self.http_session.post(
                self.login_url,
                data=credentials,
                timeout=self.timeout,
            )
        except RequestException as connection_error:
            self.logger.error("[SessionAuth] - Failed to login")
            raise connection_error

        if not 200 <= response.status_code < 300:
            # serious problem
            self.logger.error(
                "Error login at %s %d: %s",
                self.login_url,
                response.status_code,
                response.content,
            )
            raise ValueError(f"Error login {self.login_url}")


# global implemetation dict. TODO refactor with __init__subclass later like maas-engine
# plugins
AUTH_METHOD_DICT = {
    "OAuth": OAuth,
    "Basic": Basic,
    "SessionAuth": SessionAuth,
    "": Authentication,
}


def build_authentication(auth_method, config, session):
    """Authentication builder

    Args:
        auth_method (str): The oauth method (Basic, OAuth)
        config (AuthConfiguration): The config to init authentication
        session (Session): The session

    Raises:
        KeyError: _description_

    Returns:
        Authentication: The authentication instance associate to the auth method
    """

    try:
        return AUTH_METHOD_DICT[auth_method](config, session)

    except KeyError as error:
        raise KeyError(f"Not supported auth method {auth_method}") from error
