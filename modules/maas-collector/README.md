# maas-collector

maas-collector collects and extracts data from files and remote APIs to fill in a database.

## Introduction

Several types of collectors are provided by `maas_collector.rawdata.cli` package allowing to ingest data from local and remote interfaces.

To show options available for a collector, add the `-h` option to the entry point:

```bash
python3 -m maas_collector.rawdata.cli.filesystem -h
```

> See [Common options](common_options)

## Generic collectors

| Collector                                  | Entry point                             | Description                                                                                            |
| ------------------------------------------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| [](./filecollector.md)                     | `maas_collector.rawdata.cli.filesystem` | Ingest file or directory from a local file system.                                                     |
| [Ftp Collector](./ftpcollector.md)         | `maas_collector.rawdata.cli.ftp`        | Ingest file from a remote FTP server.                                                                  |
| [Jira Collector](./jiraxcollector.md)      | `maas_collector.rawdata.cli.jirax`      | Ingest data from Altlassian Jira tickets and attachments                                               |
| [Loki Collector](./lokicollector.md)       | `maas_collector.rawdata.cli.loki`       | Ingest logs from a Loki server.                                                                        |
| [MonitorCollector](./monitorcollector.md)  | `maas_collector.rawdata.cli.monitor`    | Monitor interfaces from any collector configuration to produce probes for availability monitoring. See |
|                                            | `maas_collector.rawdata.cli.odata`      | Ingest standard OData HTTP interfaces, v3 and v4 supported. Replay supported.                          |
| [R/O SFTP Collector](./rosftpcollector.md) | `maas_collector.rawdata.cli.rosftp`     | Ingest files from an SFTP server (read-only).                                                          |
| [SFTP Collector](./sftpcollector.md)       | `maas_collector.rawdata.cli.sftp`       | Ingest files from an SFTP server using writable inbox directory.                                       |
| [WebDAV Collector](./webdavcollector.md)   | `maas_collector.rawdata.cli.webdav`     | Ingest files from a WebDAV server directory.                                                           |

## Specific collectors

| Entry point                          | Collector                                                    |
| ------------------------------------ | :----------------------------------------------------------- |
| `maas_collector.rawdata.cli.mpip`    | Specific collector for ESA needs                             |
| `maas_collector.rawdata.cli.weather` | Custom collector sample / demo that ingest weather open data |

## Generic extractors

maas-collector can extract data from different formats using text configuration.

| Format | Description                        | Extractor                                   | Comments                                                                                                      |
| ------ | ---------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| csv    | comma separated values (text)      | [CSVExtractor](./csvextractor.md)           | extract data dictionaries from rows with or with headers                                                      |
| json   | JavaScript Object Notation (text)  | [JSONExtractor](./jsonextractor.md)         | extract data dictionaries using JSONPATH expressions                                                          |
| json   | JavaScript Object Notation (text)  | [JSONExtractorExtended](./jsonextractor.md) | extract data dictionaries using JSONPATH expressions with a richer but slower API than standard JSONExtractor |
| log    | Text file                          | [LogExtractor](./logextractor.md)           | extract data dictionaries per line of a text file using regular expressions                                   |
| xlsx   | Microsoft Excel Format             | [XLSXExtractor](xlsxextractor.md)           | extract data dictionaries from **rows** with or with headers                                                  |
| xlsx   | Microsoft Excel Format             | [XLSXColumnExtractor](xlsxextractor.md)     | extract data dictionaries from **columns** with or with headers                                               |
| xml    | eXtensible Mark-up Language (text) | [XMLExtractor](xmlextractor.md)             | extract data dictionaries using XPath expressions                                                             |
