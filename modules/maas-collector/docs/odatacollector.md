# OData Collector

OData collector is used to ingest data from OData web services.

## Quick start

```bash
python3 -m maas_collector.rawdata.cli.odata
```

## Command Line Options

| CLI option         | Environment variable | Description                                              |
| ------------------ | -------------------- | -------------------------------------------------------- |
| --odata-timeout    | ODATA_TIMEOUT        | Timeout in seconds                                       |
| --odata-keep-files | ODATA_KEEP_FILES     | Keep downloaded api pages (for debug). Defaults to false |

## Collector Configuration Options

| Configuration key | Description                          |
| ----------------- | ------------------------------------ |
| class             | shall be ODataCollectorConfiguration |

# Sample configuration

```json
{
  "collectors": [
    {
      "class": "ODataCollectorConfiguration",
      "id_field": ["product_id", "interface_name"],
      "routing_key": "new.raw.data.dd-product",
      "interface_name": "DD_DAS",
      "file_pattern": "DD_DAS_*.json",
      "refresh_interval": 10,
      "expected_collect_interval": 2160,
      "product_per_page": 1000,
      "odata_query_filter": "(Collection/Name eq 'SENTINEL-1' or Collection/Name eq 'SENTINEL-2' or Collection/Name eq  'SENTINEL-3' or Collection/Name eq 'SENTINEL-5P') and PublicationDate ge {publication_start_date} and PublicationDate le {publication_end_date}",
      "model": "DasProduct",
      "extractor": {
        "class": "JSONExtractor",
        "args": {
          "attr_map": {
            "product_id": "`this`.Id",
            "product_name": "`this`.Name",
            "content_length": "`this`.ContentLength",
            "publication_date": "`this`.PublicationDate",
            "start_date": "`this`.ContentDate.Start",
            "end_date": "`this`.ContentDate.End",
            "origin_date": "`this`.OriginDate",
            "modification_date": "`this`.ModificationDate",
            "interface_name": {
              "python": "lambda c: 'DD_DAS'"
            },
            "production_service_type": {
              "python": "lambda c: 'DD'"
            },
            "production_service_name": {
              "python": "lambda c: 'DAS'"
            }
          },
          "iterate_nodes": "$.value",
          "allow_partial": true
        }
      }
    }
  ]
}
```
