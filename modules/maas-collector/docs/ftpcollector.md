# FTP Collector

FTP collector is used to ingest data from an FTP server by specifying a list of directories to look into. It is possible to configure a recursive lookup.

## Quick start

```bash
python3 -m maas_collector.rawdata.cli.ftp
```

## Command Line Options

> No specific CLI option.

## Collector Configuration Options

Configuration class shall be FTPCollectorConfiguration

| Configuration key | Description                                               |
| ----------------- | --------------------------------------------------------- |
| class             | shall be FTPCollectorConfiguration                        |
| directories       | list of remote path, preferably absolute                  |
| recurse           | boolean flag to walk recursively through directories      |
| refresh_interval  | time interval between collect loop in minute (default 10) |
| timeout           | connection timeout in seconds (default 120)               |

## Credential File Options

| Configuration key | Description              |
| ----------------- | ------------------------ |
| ftp_hostname      | server name              |
| client_port       | server port (default 21) |
| client_username   | username                 |
| client password   | user password            |

## Sample configuration

```javascript
{
    "collectors": [
        {
            "class": "FTPCollectorConfiguration",
            "id_field": [
                "some_id",
                "some_date"
            ],
            "file_pattern": "*.PATTERN",
            "routing_key": "some.routing.key",
            "directories": [
                "/path/to/directory_0",
                "/path/to/directory_1",
                "/path/to/directory_2"
            ],
            "interface_name": "Test_Interface",
            "model": "SomeEntity",
            "extractor": {
                "class": "XMLExtractor",
                "args": {
                    "allow_partial": true,
                    "attr_map": {
                        "some_attr": "Parent/SubNode/Node",
                        "some_id": "Parent/SubNode/Id",
                        "some_date": "Meta/Date",
                        "interface_name": {
                            "python": "lambda c: 'Test_Interface'"
                        },
                        "production_service_type": {
                            "python": "lambda c: 'Distribution'"
                        },
                        "production_service_name": {
                            "python": "lambda c: 'Some_Service'"
                        }
                    }
                }
            }
        }
    ]
}
```
