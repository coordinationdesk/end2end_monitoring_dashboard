# File Collector

File collector is used to ingest data from a local source on a file system, either single file or directory (not recursively).

## Quick start

```bash
python3 -m maas_collector.rawdata.cli.filesystem -c collector-conf.json /path/to/file_to_ingest_1.ext /path/to/file_to_ingest_1.ext /path/to/file_to_ingest_2.ext /path/some_directory
```

## Command Line Options

| CLI option                    | Environment variable | Description                           |
| ----------------------------- | -------------------- | ------------------------------------- |
| List of positional arguments. |                      | Files or directories, space separated |

## Collector Configuration Options

> No specific option is needed as the FileCollectorConfiguration class is the parent of all configurations. Class configuration is not mandatory: File Collector uses all declared configuration to ingest data.

## Sample configuration

```javascript
{
    "collectors": [
        {
            "id_field": [
                "some_id",
                "some_date"
            ],
            "file_pattern": "*.PATTERN",
            "routing_key": "some.routing.key",
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
