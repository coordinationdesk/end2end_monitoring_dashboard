# Read Only SFTP Collector

Read Only SFTP collector is used to ingest files from an SFTP server.

Data ingestion flow is based on the modification dates of the remote files. According to these dates, files are considered either to be discriminated or to be ingested.

## Quick start

```bash
python3 -m maas_collector.rawdata.cli.rosftp
```

## Command Line Options

> No specific CLI option.

## Collector Configuration Options

| Configuration key | Description                                   |
| ----------------- | --------------------------------------------- |
| class             | shall be ReadOnlySFTPCollectorConfiguration   |
| interface_name    | name of the interface                         |
| directories       | list of directory path to watch               |
| refresh_interval  | time interval between collect loop in seconds |
| timeout           | connection timeout in seconds                 |
