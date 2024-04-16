"""
    Dummy conftest.py for maas_collector.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

from unittest.mock import Mock

from opensearchpy.connection.connections import connections as es_connections

import pytest
from requests.exceptions import ConnectionError as RequestConnectionError


@pytest.fixture
def mock_client():
    client = Mock()
    es_connections.add_connection("mock", client)
    yield client
    es_connections._conn = {}
    es_connections._kwargs = {}


class MockResponse:
    def __init__(self, json_data, status_code, content="No message"):
        self.json_data = json_data
        self.status_code = status_code
        self.content = content

    def json(self):
        return self.json_data


def mocked_requests_get(*args, **kwargs):
    if args[0].startswith("http://my_super_product_url"):
        # An other page
        return MockResponse(
            {
                "@odata.context": "$metadata#Products",
                "@odata.count": 3,
                "value": [
                    {
                        "@odata.mediaContentType": "application/octet-stream",
                        "Id": "3d5934fa-ca8a-4e74-a394-1eca3626e967",
                        "Name": "S1B_OPER_AUX_PREORB_OPOD_20211108T140148_V20211108T081548_20211108T145048.EOF.zip",
                        "ContentType": "application/octet-stream",
                        "ContentLength": 129873,
                        "PublicationDate": "2021-11-08T14:10:07.023Z",
                        "EvictionDate": "2021-11-15T14:10:07.023Z",
                        "Checksum": [
                            {
                                "Algorithm": "MD5",
                                "Value": "d0c6ba741e52f908865aaab9daa21e24",
                                "ChecksumDate": "2021-11-08T14:10:04Z",
                            }
                        ],
                        "ProductionType": "systematic_production",
                        "ContentDate": {
                            "Start": "2021-11-08T08:15:48Z",
                            "End": "2021-11-08T14:50:48Z",
                        },
                    },
                    {
                        "@odata.mediaContentType": "application/octet-stream",
                        "Id": "3d5934fa-ca8a-4e74-a394-1eca3626e967",
                        "Name": "S1B_OPER_AUX_PREORB_OPOD_20211108T140148_V20211108T081548_20211108T145048.EOF.zip",
                        "ContentType": "application/octet-stream",
                        "ContentLength": 129873,
                        "PublicationDate": "2021-11-08T14:10:07.023Z",
                        "EvictionDate": "2021-11-15T14:10:07.023Z",
                        "Checksum": [
                            {
                                "Algorithm": "MD5",
                                "Value": "d0c6ba741e52f908865aaab9daa21e24",
                                "ChecksumDate": "2021-11-08T14:10:04Z",
                            }
                        ],
                        "ProductionType": "systematic_production",
                        "ContentDate": {
                            "Start": "2021-11-08T08:15:48Z",
                            "End": "2021-11-08T14:50:48Z",
                        },
                    },
                    {
                        "@odata.mediaContentType": "application/octet-stream",
                        "Id": "3d5934fa-ca8a-4e74-a394-1eca3626e967",
                        "Name": "S1B_OPER_AUX_PREORB_OPOD_20211108T140148_V20211108T081548_20211108T145048.EOF.zip",
                        "ContentType": "application/octet-stream",
                        "ContentLength": 129873,
                        "PublicationDate": "2021-11-08T14:10:07.023Z",
                        "EvictionDate": "2021-11-15T14:10:07.023Z",
                        "Checksum": [
                            {
                                "Algorithm": "MD5",
                                "Value": "d0c6ba741e52f908865aaab9daa21e24",
                                "ChecksumDate": "2021-11-08T14:10:04Z",
                            }
                        ],
                        "ProductionType": "systematic_production",
                        "ContentDate": {
                            "Start": "2021-11-08T08:15:48Z",
                            "End": "2021-11-08T14:50:48Z",
                        },
                    },
                ],
            },
            200,
        )
    return MockResponse(None, 404, "Bad request")


def mocked_requests_work_and_fail(*args, **kwargs):
    """Work for the first req with count else fail"""
    if "$count=true" in args[0]:
        return MockResponse(
            {
                "@odata.context": "$metadata#Products",
                "@odata.count": 3,
            },
            200,
        )
    return MockResponse(None, 404, "Bad request")


def mocked_requests_post(*args, **kwargs):
    if args[0].startswith("http://my_super_token_url"):
        return MockResponse(
            {
                "access_token": "my_super_token_oauth",
                "refresh_token": "my_super_token_oauth",
                "expires_in": 60,
            },
            200,
        )
    return MockResponse(None, 404, "Bad request")


def mocked_requests_post_short_token(*args, **kwargs):
    if args[0].startswith("http://my_super_token_url"):
        return MockResponse(
            {
                "access_token": "my_super_token_oauth",
                "refresh_token": "my_super_refresh_token_oauth",
                "expires_in": 0,
            },
            200,
        )
    return MockResponse(None, 404, "Bad request")


def mocked_requests_post_short_token_failed_refresh(*args, **kwargs):
    if "grant_type=refresh_token" in kwargs["data"]:
        return MockResponse(None, 404, "Bad request")

    return MockResponse(
        {
            "access_token": "my_super_token_oauth",
            "refresh_token": "my_super_refresh_token_oauth",
            "expires_in": 0,
        },
        200,
    )


def mocked_requests_get_no_response(*args, **kwargs):
    """Raise Error"""
    raise RequestConnectionError


def mocked_requests_get_work_then_no_response(*args, **kwargs):
    """Work for the first req with count else raise error"""
    if "$count=true" in args[0]:
        return MockResponse(
            {
                "@odata.context": "$metadata#Products",
                "@odata.count": 3,
            },
            200,
        )
    else:
        raise RequestConnectionError
