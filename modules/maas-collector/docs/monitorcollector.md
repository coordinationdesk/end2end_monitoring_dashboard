# Monitor Collector

Monitor collector is used to monitor external services.

This collector generates JSON files which are later ingested with a JSON extraction configuration.

## Quick start

```bash
python3 -m maas_collector.rawdata.cli.monitor
```

## Command Line Options

| CLI option                  | Environment variable             | Description        |
| --------------------------- | -------------------------------- | ------------------ |
| --monitoring-interface-name | Name of the monitoring interface | Timeout in seconds |

## Collector Configuration Options

| Configuration key | Description                                         |
| ----------------- | --------------------------------------------------- |
| class             | shall be InterfaceMonitorCollectorConfiguration     |
| interface_name    | Name of the monitoring interface                    |
| refresh_interval  | delay between collect loop in seconds (default 300) |
| extra_http_probes | a list of arbitrary URL that will be checked        |

# Sample configuration

```json
{
  "collectors": [
    {
      "class": "InterfaceMonitorCollectorConfiguration",
      "id_field": ["interface_name", "probe_time_start"],
      "routing_key": "new.raw.data.interface-probe",
      "interface_name": "General_Monitoring",
      "file_pattern": "MAAS-Monitoring-*.json",
      "extra_http_probes": [
        {
          "interface_name": "Some_Site_To_Check_1",
          "url": "https://link_to.domain/index.html"
        },
        {
          "interface_name": "Some_Site_To_Check_2",
          "url": "https://link_to.other_domain//api/health"
        }
      ],
      "refresh_interval": 0,
      "model": "InterfaceProbe",
      "extractor": {
        "class": "JSONExtractor",
        "args": {
          "iterate_nodes": "$.results",
          "attr_map": {
            "probe_time_start": "`this`.probe_time_start",
            "probe_time_stop": "`this`.probe_time_end",
            "probe_duration": "`this`.probe_duration",
            "interface_name": "`this`.interface_name",
            "status": "`this`.status",
            "status_code": "`this`.status_code",
            "details": "`this`.details",
            "most_recent_modification_date": "`this`.most_recent_modification_date"
          }
        }
      }
    }
  ],
  "amqp": {
    "new.raw.data.interface-probe": {
      "chunk_size": 1
    }
  }
}
```
