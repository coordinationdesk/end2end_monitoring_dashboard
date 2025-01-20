# `CSVExtractor`

```{eval-rst}
:class:`maas_collector.rawdata.extractors.CsvExtractor`
` uses the :py:mod:`csv` module of the python standard library to read dictionnary from csv files.
```

> `CSVExtractor ` requires CSV files to have column headers with unique names.

## Basic usage

`CSVExtractor` requires a `attr_map` object as argument to map entity field names with CSV column names declared in the header.

Given the following extractor configuration:

```json
{
  "...": "...",
  "extractor": {
    "class": "CSVExtractor",
    "args": {
      "attr_map": {
        "satellite": "satelliteID",
        "duration": "AcquisitionDuration[msec]"
      }
    }
  }
}
```

And this input file:

```
"SatelliteID","ID","AbsoluteOrbit","RelativeOrbit","Timeliness","Scenes","AcquisitionStart","AcquisitionStop","AcquisitionDuration[msec]","EffectiveDownlinkStart","EffectiveDownlinkStop","DownlinkDuration[msec]","Latency[min]","Station","Partial"
"S2B","22858-1","22858","95","NOMINAL","84","2021-07-22T12:36:52.628","2021-07-22T12:41:55.700","303072","2021-07-22T12:52:24.854","2021-07-22T12:57:08.226","283372","15","EDRS-A"
"S2B","22858-2","22858","95","NOMINAL","23","2021-07-22T12:42:58.560","2021-07-22T12:44:21.544","82984","2021-07-22T12:57:08.226","2021-07-22T12:58:25.816","77590","14","EDRS-A"
"S2B","22858-3","22858","95","NOMINAL","20","2021-07-22T12:50:30.675","2021-07-22T12:51:42.835","72160","2021-07-22T12:58:25.816","2021-07-22T12:59:33.285","67469","7","EDRS-A"
```

The extractor will extract the following objects:

```python
[
    {
        "satellite":  "S2B",
        "duration": "303072",

    },
    {
        "satellite":  "S2B",
        "duration": "82984",

    },
    {
        "satellite":  "S2B",
        "duration": "72160",

    }
]
```
