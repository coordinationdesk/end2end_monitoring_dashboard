# Simple Http Collector (Used in spaceops projects to collect spacetrack data)

Simple Http collector is used to ingest data from spacetrack web services **[Spacetrack web services](https://www.space-track.org/)**.

## Quick start

```bash
TZ=UTC python3.11 -m maas_collector.rawdata.cli.simplehttp -d $WORK_DIR/maas-deploy-soserver/configuration/collector/spacetrack/ --healthcheck-port 31400 -p 0 -v --credential-file "<path to credential-file.json>"
```

## Command Line Options

| CLI option               | Environment variable       | Description                                              |
| ------------------------ | -------------------------- | -------------------------------------------------------- |
| --http-common-timeout    | HTTP_COMMON_TIMEOUT        | Timeout in seconds                                       |
| --http-common-keep-files | HTTP_COMMON_KEEP_FILES     | Keep downloaded api pages (for debug). Defaults to false |

## Collector Configuration Options

| Configuration key | Description                              |
| ----------------- | ----------------------------------------- |
| class             | shall be SimpleHttpCollectorConfiguration |

## Sample collector credential configuration

```json
{
    "name": "space-track-tle-data",
    "product_url": "https://www.space-track.org",
    "login_url": "https://www.space-track.org/ajaxauth/login",
    "http_rest_uri": "/basicspacedata/query/class/gp/EPOCH/>now-1/orderby/NORAD_CAT_ID,EPOCH,CREATION_DATE/format/json",
    "credentials": {
        "identity": "username",
        "password": "xxxxx"
    }
    // where is credentials dictionary of the dict form:
    //             {
    //                 "username_field": "username",
    //                 "password_field": "password"
    //             }
    //             where:
    //             - username_field (str): The expected form field name for the user's identifier.
    //             - password_field (str): The expected form field name for the user's password.
    //             - username (str): The user's identifier or username.
    //             - password (str): The user's password.
}
```

## Sample collector configuration

```json
{
    "collectors": [
        {
            "class": "SimpleHttpCollectorConfiguration",
            "id_field": [
                "international_designator",
                "creation_date"
            ],
            "routing_key": "new.raw.space.track.tle.object",
            "interface_name": "space-track-tle-data",
            "file_pattern": "space-track-tle-data-*.json",
            "refresh_interval": 0,
            "expected_collect_interval": 86400,
            "end_date_time_offset": 0,
            "model": "SpacetrackTle",
            "protocol_version": "v1",
            "extractor": {
                "class": "JSONExtractor",
                "args": {
                    "attr_map": {
                        "ccsds_omm_vers": "CCSDS_OMM_VERS",
                        "comment": "COMMENT",
                        "creation_date": "CREATION_DATE",
                        "originator": "ORIGINATOR",
                        "name": "OBJECT_NAME",
                        "international_designator": "OBJECT_ID",
                        "center_name": "CENTER_NAME",
                        "ref_frame": "REF_FRAME",
                        "time_system": "TIME_SYSTEM",
                        "mean_element_theory": "MEAN_ELEMENT_THEORY",
                        "tle_date": "EPOCH",
                        "mean_motion": "MEAN_MOTION",
                        "eccentricity": "ECCENTRICITY",
                        "inclination": "INCLINATION",
                        "ra_of_asc_node": "RA_OF_ASC_NODE",
                        "arg_of_pericenter": "ARG_OF_PERICENTER",
                        "mean_anomaly": "MEAN_ANOMALY",
                        "ephemeris_type": "EPHEMERIS_TYPE",
                        "classification_type": "CLASSIFICATION_TYPE",
                        "norad_designator": "NORAD_CAT_ID",
                        "element_set_no": "ELEMENT_SET_NO",
                        "rev_at_epoch": "REV_AT_EPOCH",
                        "b_star": "BSTAR",
                        "mean_motion_dot": "MEAN_MOTION_DOT",
                        "mean_motion_ddot": "MEAN_MOTION_DDOT",
                        "semimajor_axis": "SEMIMAJOR_AXIS",
                        "period": "PERIOD",
                        "apoapsis": "APOAPSIS",
                        "periapsis": "PERIAPSIS",
                        "object_type": "OBJECT_TYPE",
                        "rcs_size": "RCS_SIZE",
                        "country_code": "COUNTRY_CODE",
                        "launch_date": "LAUNCH_DATE",
                        "site": "SITE",
                        "decay_date": "DECAY_DATE",
                        "file": "FILE",
                        "gp_id": "GP_ID",
                        "tle_line0": "TLE_LINE0",
                        "tle_line1": "TLE_LINE1",
                        "tle_line2": "TLE_LINE2"
                    },
                    "iterate_nodes": "$",
                    "allow_partial": true
                }
            }
        }
    ],
    "amqp": {
        "new.raw.space.track.tle.object": {
            "chunk_size": 640
        }
    }
}
```
