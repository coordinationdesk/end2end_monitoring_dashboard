# MAAS-Collector Development log

## elementtree limitations

Once you get a xml element with `find` method, you cannot access the parent node. That made the implementation of ESIP file extractor requires a specific class because generic `XMLExtractor` was not able to handle it. Hopefully, that was really easy.

## Using minio with boto3

### Change detection

Change detection is accomplished by listening to ampq messages `new.raw.data payload` with the following payload:

```json
{
    "EventName": "s3:ObjectCreated:Put",
    "Key": "rawdata/raw-data-pripapi-query.json",
    "Records": [
        {
            "eventVersion": "2.0",
            "eventSource": "minio:s3",
            "awsRegion": "",
            "eventTime": "2021-08-18T13:01:37.174Z",
            "eventName": "s3:ObjectCreated:Put",
            "userIdentity": {
                "principalId": "maasminio"
            },
            "requestParameters": {
                "principalId": "maasminio",
                "region": "",
                "sourceIPAddress": "10.1.149.98"
            },
            "responseElements": {
                "content-length": "0",
                "x-amz-request-id": "169C682A8C3876F6",
                "x-minio-deployment-id": "94fd2308-ab86-4f6a-a0d7-0dfb1b31385c",
                "x-minio-origin-endpoint": ""
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "Config",
                "bucket": {
                    "name": "rawdata",
                    "ownerIdentity": {
                        "principalId": "maasminio"
                    },
                    "arn": "arn:aws:s3:::rawdata"
                },
                "object": {
                    "key": "raw-data-pripapi-query.json",
                    "size": 1017,
                    "eTag": "b56723a3908772e7b9cd931d530f57cc",
                    "contentType": "application/octet-stream",
                    "userMetadata": {
                        "content-type": "application/octet-stream",
                        "x-minio-internal-inline-data": "true",
                        "x-minio-internal-tier-free-versionID": "22803855-6538-4c50-b48e-b4cd73d0fde2"
                    },
                    "sequencer": "169C682A8D9B6F26"
                }
            },
            "source": {
                "host": "10.1.149.98",
                "port": "",
                "userAgent": "MinIO (linux; amd64) minio-go/v7.0.12"
            }
        }
    ]
}
```

### File download

Downloading file from s3 bucket is rather straightforward:

```python

import boto3

from botocore.client import Config

s3 = boto3.resource('s3',
    endpoint_url='http://s3.maas.telespazio.corp',
    aws_access_key_id='maasminio',
    aws_secret_access_key='maasminio',
    config=Config(signature_version='s3v4'),
)

s3.Bucket("rawdata").download_file("raw-data-pripapi-query.json", "/tmp/pripapi-query.json")

```

# TODO: File prioritization strategy

Finding the right order to ingest files is complicated: naive approach to ingest the latest will make the dashboard unsuitable for close-time monitoring.

Most files have a date in their name. By extracting this timestamp and using the [heapq](https://docs.python.org/3.9/library/heapq.html) module, it is possible to easily maintain a list prioritized by 1 / timestamp to always process recent files.

Implementation will be an iterator that will refresh every x seconds by listing files, and also refresh at exhausting.

# TODO: Python fields

Python-powered fields only accept XML or JSON node as argument, making hard or impossible to make calculated fields based on existing extracted values.

For some calculated fields, a drastically better option is to pass the already extracted dictionary as argument (or in the local namespace as well named variables).s