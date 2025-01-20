# WebDAV Collector

WebDAV collector is used to ingest data from a WebDAV file server.

## Quick start

```bash
python3 -m maas_collector.rawdata.cli.webdav
```

## Command Line Options

| CLI option       | Environment variable | Description        |
| ---------------- | -------------------- | ------------------ |
| --webdav-timeout | WEBDAV_TIMEOUT       | Timeout in seconds |

## Collector Configuration Options

| Configuration key                | Description                                                                                                  |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| class                            | shall be WebDAVCollectorConfiguration                                                                        |
| client_url                       | URL of the WebDAV server                                                                                     |
| depth                            | WebDAV search argument. Default to "infinite" for recursive search ; if not supported by the server, use "1" |
| auth_method                      | Authentication method                                                                                        |
| token_field_header               | Custom HTTP header added for authentication query                                                            |
| client_username                  | User name                                                                                                    |
| client_password                  | User password                                                                                                |
| interface_name                   | Name of the interface                                                                                        |
| directories                      | List of directory names to watch                                                                             |
| disable_insecure_request_warning | Flag to bypass HTTP certificate verification. Strongly not recommended for security concerns.                |
| refresh_interval                 | time interval between collect loop in seconds                                                                |
