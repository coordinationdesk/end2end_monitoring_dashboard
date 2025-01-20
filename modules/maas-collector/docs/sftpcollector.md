# SFTP Collector

SFTP collector is used to ingest files from an SFTP server where files:

- are writable
- are collected from multiple inbox directories
- are moved to directories after ingestion depending on the ingestion result (ingested or rejected)

## Quick start

```bash
python3 -m maas_collector.rawdata.cli.sftp
```

## Command Line Options

| CLI option            | Environment variable | Description                                                                                          |
| --------------------- | -------------------- | ---------------------------------------------------------------------------------------------------- |
| --sftp-hostname       | SFTP_HOSTNAME        | SFTP hostname                                                                                        |
| --sftp-port           | SFTP_PORT            | SFTP port                                                                                            |
| --sftp-username       | SFTP_USERNAME        | Username                                                                                             |
| --sftp-password       | SFTP_PASSWORD        | Password                                                                                             |
| --sftp-process-prefix | SFTP_PROCESS_PREFIX  | File prefix for processing file (default: ".maas-process-")                                          |
| --sftp-inbox-root     | SFTP_INBOX_ROOT      | Root directory of the inbox                                                                          |
| --sftp-ingested-dir   | SFTP_INGESTED_DIR    | Directory to store successfully ingested files (default: INGESTED)                                   |
| --sftp-rejected-dir   | SFTP_REJECTED_DIR    | Directory to store successfully rejected files (default: REJECTED)                                   |
| --sftp-force-suffix   | SFTP_FORCE_SUFFIX    | File suffix for forcing file ingestion (default: .MAAS-FORCE)                                        |
| --sftp-age-limit      | SFTP_AGE_LIMIT       | Age limit in seconds for a file to be considered abandoned and ingested again (default: 900 seconds) |
| argument list         |                      | list of directories to watch in the inbox root                                                       |

## Collector Configuration Options

| Configuration key | Description                                   |
| ----------------- | --------------------------------------------- |
| class             | shall be SFTPCollectorConfiguration           |
| interface_name    | name of the interface                         |
| refresh_interval  | time interval between collect loop in seconds |
| timeout           | connection timeout in seconds                 |
