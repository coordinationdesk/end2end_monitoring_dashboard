# Loki Collector

Loki collector is used to ingest data from a Loki log server.

## Quick start

```bash
python3 -m maas_collector.rawdata.cli.loki
```

## Command Line Options

| CLI option        | Environment variable | Description                                   |
| ----------------- | -------------------- | --------------------------------------------- |
| --loki-timeout    | LOKI_TIMEOUT         | Timeout in seconds                            |
| --loki-keep-files | LOKI_KEEP_FILES      | Flag to keep file locally (for debug purpose) |

## Collector Configuration Options

| Configuration key    | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| class                | shall be LokiCollectorConfiguration                         |
| date_attr            | Name of a date attribute for key generation                 |
| refresh_interval     | time interval between collect loop in seconds (default 720) |
| max_time_window      | width of the time window                                    |
| query                | Loki query                                                  |
| query_limit          | maximum number of log lines                                 |
| query_prefix         | A prefix added to queries to simplify URL for deployment    |
| protocol_version     | Defaults to v1                                              |
| end_date_time_offset | An offset added to the end date argument. Defaults to zero  |

# Sample configuration

```json
{
  "collectors": [
    {
      "class": "LokiCollectorConfiguration",
      "id_field": ["access_date", "interface_name", "user"],
      "routing_key": "new.raw.data.grafana-usage",
      "interface_name": "Grafana_Usage_Prod",
      "file_pattern": "Grafana_Usage_Prod_*.json",
      "refresh_interval": 30,
      "expected_collect_interval": 10080,
      "max_time_window": 30,
      "query": "{job=\"some-namespace/grafana\"} |= `logger=context` |= `Request Completed` |~ `path=/api/dashboards/uid|path=/api/dashboards/home` | logfmt",
      "query_limit": 5000,
      "query_prefix": "/loki/api/v1/query_range",
      "model": "GrafanaUsage",
      "product_url": "http://loki-stack.monitoring.svc.cluster.local:3100",
      "protocol_version": "v1",
      "extractor": {
        "class": "JSONExtractor",
        "args": {
          "attr_map": {
            "user": "`this`.stream.uname",
            "access_date": "`this`.stream.t",
            "dashboard": "`this`.stream.path",
            "interface_name": {
              "python": "lambda c: 'Grafana_Usage_Prod'"
            }
          },
          "iterate_nodes": "$.data.result",
          "allow_partial": true
        }
      }
    }
  ]
}
```
