# `XLSXExtractor`

```{eval-rst}
:class:`maas_collector.rawdata.extractors.XlsxExtractor`
` uses the :py:mod:`xlsx` module of the python standard library to read dictionnary from xlsx files.
```

> `XLSXExtractor` requires XLSX files to have column attribut with unique names.

## Basic usage

`XLSXExtractor` requires a `attr_map` object as argument to map entity field names with XLSX names declared in the first line.

Given the following extractor configuration:

```json
{
  "...": "...",
  "extractor": {
    "class": "XLSXExtractor",
    "args": {
        "attr_map": {
            "satellite_id": "Satellite",
            "doy": "DOY",
            "downlink_orbit": "Downlink Orbit",
            "antenna_id": "Antenna ID",
            "antenna_satus": "Antenna status (OK/NOK)",
            "front_end_id": "Front End Id",
            "front_end_status": "Front End Status",
            "planned_data_start": "Planned Data Start",
            "planned_data_stop": "Planned Data Stop",
            "interface_name": {
                "python": "lambda root: 'DDP_MPS-Maspalomas'"
            },
            "production_service_type": {
                "python": "lambda root: 'DDP'"
            },
            "production_service_name": {
                "python": "lambda root: 'MPS-Maspalomas'"
            }
        }
    }
}
```

And this input file:

| Item# | DOY | Satellite   | Downlink Orbit | Antenna ID | Antenna status (OK/NOK) | Front End Id                                                     | Front End Status | Planned Data Start  | Planned Data Stop   |
| ----- | --- | ----------- | -------------- | ---------- | ----------------------- | ---------------------------------------------------------------- | ---------------- | ------------------- | ------------------- |
| 1     | 141 | SENTINEL-2A | 36102          | ALVA       | OK                      | CORTEXHDR4,CORTEXHDR5,CORTEXHDR5-SEND,CORTEXHDR6,CORTEXHDR6-SEND | OK               | 2022-05-21T17:03:42 | 2022-05-21T17:03:42 |
| 2     | 141 | SENTINEL-2B | 27194          | SIV        | OK                      | CORTEXHDR4,CORTEXHDR5,CORTEXHDR5-SEND,CORTEXHDR6,CORTEXHDR6-SEND | OK               | 2022-05-21T17:53:20 | 2022-05-21T17:59:33 |
| 3     | 141 | SENTINEL-2A | 36103          | ALVA       | OK                      | CORTEXHDR4,CORTEXHDR5,CORTEXHDR5-SEND,CORTEXHDR6,CORTEXHDR6-SEND | OK               | 2022-05-21T18:43:16 | 2022-05-21T18:51:12 |

The extractor will extract the following objects:

```python
[
    {
        "satellite_id": "SENTINEL-2A",
        "doy": 141,
        "downlink_orbit": 36102,
        "antenna_id": "ALVA",
        "antenna_satus": "OK",
        "front_end_id": "CORTEXHDR4,CORTEXHDR5,CORTEXHDR5-SEND,CORTEXHDR6,CORTEXHDR6-SEND",
        "front_end_status": "OK",
        "planned_data_start": "2022-05-21T17:03:42",
        "planned_data_stop": "2022-05-21T17:03:42",
        "interface_name" : "DDP_MPS-Maspalomas",
        "production_service_type" : "DDP",
        "production_service_name" : "MPS-Maspalomas"
    },
    {
        "satellite_id": "SENTINEL-2B",
        "doy": 141,
        "downlink_orbit": 27194,
        "antenna_id": "SIV",
        "antenna_satus": "OK",
        "front_end_id": "CORTEXHDR4,CORTEXHDR5,CORTEXHDR5-SEND,CORTEXHDR6,CORTEXHDR6-SEND",
        "front_end_status": "OK",
        "planned_data_start": "2022-05-21T17:53:20",
        "planned_data_stop": "2022-05-21T17:59:33",
        "interface_name" : "DDP_MPS-Maspalomas",
        "production_service_type" : "DDP",
        "production_service_name" : "MPS-Maspalomas"
    },
    {
        "satellite_id": "SENTINEL-2A",
        "doy": 141,
        "downlink_orbit": 36103,
        "antenna_id": "ALVA",
        "antenna_satus": "OK",
        "front_end_id": "CORTEXHDR4,CORTEXHDR5,CORTEXHDR5-SEND,CORTEXHDR6,CORTEXHDR6-SEND",
        "front_end_status": "OK",
        "planned_data_start": "2022-05-21T18:43:16",
        "planned_data_stop": "2022-05-21T18:51:12",
        "interface_name" : "DDP_MPS-Maspalomas",
        "production_service_type" : "DDP",
        "production_service_name" : "MPS-Maspalomas"
    }
]
```
