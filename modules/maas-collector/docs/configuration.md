# Collector Configuration

maas-collector uses JSON file to store:

- a list of configurations in the root key `collectors`
- amqp fine-tuning in the root key `amqp`

```json
{
  "collectors": [
    {
      "id_field": "...",
      "file_pattern": "...",
      "routing_key": "...",
      "model": {},
      "extractor": {}
    }
  ],
  "amqp": {
    "some.routing.key": {
      "chunk_size": 512
    }
  }
}
```

## Collector configuration

A collector configuration is a JSON object containing the following keys:

`id_field`
: Name of the data attribute that will be used as a unique identifier. It can be a _single string_ or a _list of string_ whose values will be hashed to create a composite identifier in a deterministic way.

`file_pattern`
: A string providing a pattern to match a filename. It shall be compatible with the python module `fnmatch` available in the standard library.

`routing_key`
: A string providing the AMPQ queue name to emit message after model entity creation in the raw storage.

`model`
: An object describing the OpenSearch document model. See below for details.

`extractor`
: An object describing the extractor configuration. See below for details.

### Model configuration

Model configuration is stored in an object with the following keys:

`index`
: Name of the OpenSearch index to store extracted objects

`name`
: Name of the document class that will be dynamically created in Python.

`fields`
: List of field description object containing two keys: `name` string for the attribute name and `type` string for attribute type. `type` value shall be a class name available in the `opensearchpy.field` module.

`partition_field`
: Optional date field name used to create the index partition name. Defaults to `ingestionTime` model attribute.

`partition_format`
: Optional `datetime.strftime` compatible format string like`%Y-%m` used to create the partition name. Defaults to `%Y`.

### Model configuration sample

```json
{
  "...": "...",
  "model": {
    "index": "es-sample-index-name",
    "name": "SampleModelClass",
    "partition_field": "fieldName2",
    "partition_format": "%Y-%m",
    "fields": [
      {
        "name": "fieldName1",
        "type": "Keyword"
      },
      {
        "name": "fieldName2",
        "type": "Date"
      },
      {
        "name": "fieldName3",
        "type": "Long"
      }
    ]
  },
  "...": "..."
}
```

## Zulu Date

`Date` fields are automatically replaced by a custom `ZuluDate` class instance to ensure correct serialization of any `datetime` data to Zulu string format.

## Extractor configuration

Extractors are configured by setting a `class` key in the `extractor` object of the configuration and a set of keys in a `args` object:

```json
{
  "...": "...",
  "extractor": {
    "class": "SampleExtractor",
    "args": {
      "custom_arg1": 42,
      "custom_arg2": "jdoe"
    }
  },
  "...": "..."
}
```

## Extractor implementations

Current implementation provides three generic extractors to ingest some common text formats:

- [XMLExtractor](xmlextractor) extracts data from XML document using xpath
- [JSONExtractor](jsonextractor) extracts data from JSON document using json-path
- [LogExtractor](logextractor) extracts data from text log file lines using python regex
- [CSVExtractor](csvextractor) extracts data from comma-separated-value file
- [XLSXExtractor](xlsxextractor) extracts data from XLSX document using xpath

### Custom extractor implementation

For some special cases, custom implementations are easy to code by implementing an abstract class `BaseExtractor` that only requires to implement the `extract(path:str)` generator method (see custom extractor development guide).

## AMQP message grouping configuration

By default, if a `routing_key` is not empty for a collector configuration, a message will be sent on the `amqp` bus for _each_ entity inserts or updates.

To group the identifiers provided by extraction,

```json
{
  "collectors": [
    {
      "id_field": "...",
      "file_pattern": "...",
      "routing_key": "...",
      "model": {},
      "extractor": {}
    }
  ],
  "amqp": {
    "some.routing.key": {
      "chunk_size": 512
    }
  }
}
```
