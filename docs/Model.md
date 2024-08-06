# Database model description

## Nomenclature

The name of datasources provides information of the date used for the index partitioning

- `*-monitoring`: no partitioning filter uses, searches are done on all indices with an alias, and with the `updateTime` time field
- `*-sensing`: searches by the sensing start date
- `*-publication`: searches by the publication date

## Indices

- `raw-data-*` indices are the raw data collected. All field map to the fields found on the payload downloaded on external interfaces
- `cds-*` indices are consolidated data by OMCS dashboard services

> `Type` in following table are :
> * E for Elasticsearch indices,
>     - the time field match the partitioning in the database
> * G for Data source on Grafana,
>     - the time field match the field use in Grafana timeline to request data

| Index                             | Type | Time Field               | Description                                                                                                                                 |
|-----------------------------------|------|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| cds-publication                   | EG   | sensing_start_date       | Direct consolidation of raw-data with additional field extracted (mission, satellite,product_type...). Granularity with raw-data is 1 to 1. |
| cds-publication-monitoring        | G    | updateTime               | -                                                                                                                                           |
| cds-publication-publication       | G    | publication_date         | -                                                                                                                                           |
| cds-product                       | EG   | sensing_start_date       | Products are consolidation grouping publications related to the same product. Additional information are computed                           |
| cds-product-monitoring            | G    | updateTime               | -                                                                                                                                           |
| cds-product-publication           | G    | publication_date         | -                                                                                                                                           |
| cds-datatake                      | EG   | observation_time_start   | All completeness and timeliness computed field for S1 and S2 datatakes                                                                      |
| cds-datatake-monitoring           | G    | updateTime               | -                                                                                                                                           |
| cds-datatake-publication          | G    | publication_date         | -                                                                                                                                           |
| cds-downlink-datatake             | EG   | effective_downlink_start | Downlink plan for S1 and S2                                                                                                                 |
| cds-downlink-datatake-monitoring  | G    | updateTime               | -                                                                                                                                           |
| cds-s3-completeness               | EG   | observation_time_start   | All completeness and timeliness computed field for S3 orbits                                                                                |
| cds-s3-completeness-monitoring    | G    | updateTime               | -                                                                                                                                           |
| cds-s3-completeness-publication   | G    | publication_date         | -                                                                                                                                           |
| cds-s5-completeness               | EG   | observation_time_start   | All completeness and timeliness computed field for S5 orbits                                                                                |
| cds-s5-completeness-monitoring    | G    | updateTime               | -                                                                                                                                           |
| cds-s5-completeness-publication   | G    | publication_date         | -                                                                                                                                           |
| cds-sat-unavailability            | EG   | start_time               | Consolidated satellites unavailability from published reports at the AUXIP                                                                  |
| cds-sat-unavailability-monitoring | G    | updateTime               | -                                                                                                                                           |
| cds-interface-status-monitoring   | G    | status_time_start        | External interfaces availability monitoring status                                                                                          |
| raw-data-aps-product              | EG   | ingestionTime            | Give the status of all acquisition passes status from XBAND                                                                                 |
| raw-data-aps-product-edrs         | EG   | ingestionTime            | Give the status of all acquisition passes status from EDRS                                                                                  |
| cds-ddp-data-available            | EG   | time_created             | Provides DSIB information about passes transfers time and data volume                                                                       |
| maas-collector-journal            | EG   | last_date                | Journal of collection for external interface. Provide the date of last collect and the date of last product collected.                      |
| cds-dataflow-conf                 | EG   | none                     | Static table that contains the list of product type and diffusion informations                                                              |
