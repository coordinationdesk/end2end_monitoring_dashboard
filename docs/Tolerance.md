# Engine Configuration

## Tolerance

In configuration file for engine, it is possible to add a configuration for completeness tolerance.

### Configuration example

Example of completeness tolerance :

```json
"completeness_tolerance": {
    "S1": {
        "global": 0,
        "local": {
            ".*0.*": 0,
            ".*1.*": 0,
            ".*2.*": 0,
            "default": 0
        }
    },
    "S2": {
        "global": {
            "DS.*": 0,
            "GR.*": 0,
            "TL.*": 0,
            "TC.*": 0,
            "default": 0
        },
        "local": {
            ".*0.*DS": 0,
            ".*0.*GR": 0,
            ".*1.*DS": 0,
            ".*1.*GR": 0,
            ".*1.*TL": 0,
            ".*1.*TC": 0,
            ".*2.*TL": 0,
            ".*2.*TC": 0,
            ".*2.*DS": 0,
            "L0.*": 0,
            "L1.*": 0,
            "L2.*": 0,
            "default": 0
        },
        "final": 0
    },
    "S3": {
        "global": 0,
        "local": {
            ".*0.*": 0,
            ".*1.*": 0,
            ".*2.*": 0,
            "default": 0
        }
    }
}
```

### Configuration value example

This Configuration values impact expected values in datatake product.

#### Example

Example of datatake product :

```json
{
 "_index": "cds-datatake-2022-05",
 "_type": "_doc",
 "_id": "S1A-337854",
 "_version": 11,
 "_seq_no": 23368,
 "_primary_term": 5,
 "found": true,
 "_source": {
  "name": "S1A_MP_ACQ__L0__20220509T160000_20220521T180000.csv",
  "key": "S1A-337854",
  "datatake_id": "337854",
  "satellite_unit": "S1A",
  "mission": "S1",
  "observation_time_start": "2022-05-11T16:54:46.081Z",
  "observation_duration": 700601000,
  "observation_time_stop": "2022-05-11T17:06:26.682Z",
  "l0_sensing_duration": 702688000,
  "l0_sensing_time_start": "2022-05-11T16:54:44.780Z",
  "l0_sensing_time_stop": "2022-05-11T17:06:27.468Z",
  "absolute_orbit": 43166,
  "relative_orbit": 44,
  "polarization": "DV",
  "timeliness": "NRT-PT",
  "instrument_mode": "IW",
  "instrument_swath": "0",
  "application_date": "2022-05-09T16:00:00.000Z",
  "updateTime": "2022-05-11T18:35:52.795Z",
  "IW_RAW__0A_local_value": 702178000,
  "IW_RAW__0A_local_expected": 701688000,
  "IW_RAW__0A_local_value_adjusted": 701688000,
  "IW_RAW__0A_local_percentage": 100,
  "IW_RAW__0A_local_status": "Complete",
  "IW_RAW__0C_local_value": 702178000,
  "IW_RAW__0C_local_expected": 701688000,
  "IW_RAW__0C_local_value_adjusted": 701688000,
  "IW_RAW__0C_local_percentage": 100,
  "IW_RAW__0C_local_status": "Complete",
  "IW_RAW__0N_local_value": 702178000,
  "IW_RAW__0N_local_expected": 701688000,
  "IW_RAW__0N_local_value_adjusted": 701688000,
  "IW_RAW__0N_local_percentage": 100,
  "IW_RAW__0N_local_status": "Complete",
  "IW_RAW__0S_local_value": 702178000,
  "IW_RAW__0S_local_expected": 701688000,
  "IW_RAW__0S_local_value_adjusted": 701688000,
  "IW_RAW__0S_local_percentage": 100,
  "IW_RAW__0S_local_status": "Complete",
  "IW_SLC__1A_local_value": 702873000,
  "IW_SLC__1A_local_expected": 700601000,
  "IW_SLC__1A_local_value_adjusted": 700601000,
  "IW_SLC__1A_local_percentage": 100,
  "IW_SLC__1A_local_status": "Complete",
  "IW_SLC__1S_local_value": 702873000,
  "IW_SLC__1S_local_expected": 700601000,
  "IW_SLC__1S_local_value_adjusted": 700601000,
  "IW_SLC__1S_local_percentage": 100,
  "IW_SLC__1S_local_status": "Complete",
  "IW_GRDH_1A_local_value": 702812000,
  "IW_GRDH_1A_local_expected": 700601000,
  "IW_GRDH_1A_local_value_adjusted": 700601000,
  "IW_GRDH_1A_local_percentage": 100,
  "IW_GRDH_1A_local_status": "Complete",
  "IW_GRDH_1S_local_value": 702812000,
  "IW_GRDH_1S_local_expected": 700601000,
  "IW_GRDH_1S_local_value_adjusted": 700601000,
  "IW_GRDH_1S_local_percentage": 100,
  "IW_GRDH_1S_local_status": "Complete",
  "IW_OCN__2A_local_value": 0,
  "IW_OCN__2A_local_expected": 0,
  "IW_OCN__2A_local_value_adjusted": 0,
  "IW_OCN__2A_local_status": "Unknown",
  "IW_OCN__2S_local_value": 0,
  "IW_OCN__2S_local_expected": 0,
  "IW_OCN__2S_local_value_adjusted": 0,
  "IW_OCN__2S_local_status": "Unknown",
  "sensing_global_value": 5609156000,
  "sensing_global_expected": 5613156000,
  "sensing_global_value_adjusted": 5609156000,
  "sensing_global_percentage": 99.92873884139333,
  "sensing_global_status": "Partial"
 }
}
```

If we want to add one second tolerance for mission S1 and product type with level 0 (IW_RAW__0A, IW_RAW__0C etc ...) the configuration must be :

```json
"completeness_tolerance": {
    "S1": {
        "local": {
            ".*0.*": 1000000,
            ".*1.*": 0,
            ".*2.*": 0,
            "default": 0
        }
    }
}
```

Where ".\*0.\*" is a regular expression who match with product type with level 0.

The expected will become:

```json
{
  "IW_RAW__0A_local_expected": 700688000,
  "IW_RAW__0C_local_expected": 700688000,
  "IW_RAW__0N_local_expected": 700688000,
  "IW_RAW__0S_local_expected": 700688000,
}
```

### Configuration unit

| mission | product type | unit        |
|---------|--------------|-------------|
| S1      | All          | microsecond |
| S2      | DS           | microsecond |
|         | GR           | number      |
|         | TL           | number      |
|         | TC           | number      |
| S3      | TBD          | TBD         |
