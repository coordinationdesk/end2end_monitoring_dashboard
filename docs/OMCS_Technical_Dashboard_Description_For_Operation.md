
## Acquisition passes status (from EDRS)[🔗](https://omcs.copernicus.eu/grafana/d/KoNYADm4z/acquisition-passes-status-from-edrs)

**Section**: Acquisition

**Description**: 

This dashboard features Acquisition passes status.

Information is available for the following missions: S1 and S2.

Time reference for this dashboard is : planned_link_session_start

Report Type Logic : 
- If a document has been extracted from a daily report but not from a weekly or monthly report, it will be visible if 'daily' is selected
- If a document has been extracted from a weekly report but not from a monthly report, il will be visible if 'weekly' is selected
- If the same document has been extracted from multiple source, it will be available through the best source. Eg: To see a document retrieved from a weekly and a monthly source, you have to select 'monthly'
- 2 document are considered equal for the report_type logic if they have the same link_session_id and the same ground_station
- It is possible to find where the document originate from through the field 'report_name_daily' 'report_name_weekly' and 'report_name_monthly'


Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Acquisition Planned Downlinks[🔗](https://omcs.copernicus.eu/grafana/d/RIn0sd37z/acquisition-planned-downlinks)

**Section**: Acquisition

**Description**: 

This dashboard features Planned Downlink Acquisition.

Information is taken from Mission Plannings.

Information is available for the following missions: S1 and S2.

Time reference for this dashboard is : effective_downlink_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Station Acquisition Status (CADIP)[🔗](https://omcs.copernicus.eu/grafana/d/zaqHaGu4z/station-acquisition-status-cadip)

**Section**: Acquisition

**Description**: 

This dashboard features Downlink Acquisition status.

Information is taken from station reports made available through CADIP interface.

Information is available for the following missions: S1, S2 and S3.

Time reference for this dashboard is : planned_data_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Station Acquisition Status (EDS)[🔗](https://omcs.copernicus.eu/grafana/d/y7tck1D4k/station-acquisition-status-eds)

**Section**: Acquisition

**Description**: 

This dashboard features Downlink Acquisition Status.

Information is taken from station reports available from EDS ftp server.

Information is available for the missions S1 and S2.

Time reference for this dashboard is : downlink_start_time

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Station Acquisition Status (X-Band)[🔗](https://omcs.copernicus.eu/grafana/d/GP4Naujnk/station-acquisition-status-x-band)

**Section**: Acquisition

**Description**: 

This dashboard features Downlink Acquisition status.

Information is taken from station reports made available through XBAND interface.

Information is available for the following missions: S1, S2, S3 and S5

Time reference for this dashboard is : planned_data_start

Report Type Logic : 
- If a document has been extracted from a daily report but not from a weekly or monthly report, it will be visible if 'daily' is selected
- If a document has been extracted from a weekly report but not from a monthly report, il will be visible if 'weekly' is selected
- If the same document has been extracted from multiple source, it will be available through the best source. Eg: To see a document retrieved from a weekly and a monthly source, you have to select 'monthly'
- 2 document are considered equal for the report_type logic if they have the same link_session_id and the same ground_station
- It is possible to find where the document originate from through the field 'report_name_daily' 'report_name_weekly' and 'report_name_monthly'
- Report Type Monthly and Weekly are available only for S5

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Anomaly correlation follow-up[🔗](https://omcs.copernicus.eu/grafana/d/cDsbRok4z/anomaly-correlation-follow-up)

**Section**: Anomalies

**Description**: 

This dashboard features the Anomaly correlation follow-up

Information is available for the following missions: S1, S2, S3 and S5

Information is displayed through the following panels:

- Number of observation issue linked to an anomaly

Time reference for this dashboard is : observation_time_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## CAMS issue list[🔗](https://omcs.copernicus.eu/grafana/d/j-DkP4Cnz/cams-issue-list)

**Section**: Anomalies

**Description**: 

This dashboard features the list CAMS issue retrieved from JIRA.

Information is displayed through the following panels:
 - The creation of tickets is displayed in the form of a time series with the number of tickets created for each time frame;
 - List of tickets .

 Note: the time range filter on the tickets updated over the period, so if the ticket was created and updated outside this period it will not be visible

Time reference for this dashboard is : updated

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## ADG Completeness (vs external providers)[🔗](https://omcs.copernicus.eu/grafana/d/adg-completeness/adg-completeness-vs-external-providers)

**Section**: Completeness

**Description**: 

This dashboard features a completeness by product_type between product published at AUXIP and theorical daily production

Details of theorical production used in dashboard :

S1:```json[{'product_type': 'AUX_WND', 'product_type_expected': 182.0, 'timeliness': '10 min'}, {'product_type': 'AUX_ICE', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'AUX_TEC', 'product_type_expected': 1.0, 'timeliness': 'N/A'}, {'product_type': 'AUX_TRO', 'product_type_expected': 4.0, 'timeliness': '30 min'}, {'product_type': 'MPL_ORBPRE', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'MPL_ORBRES', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'MPL_TLEPRE', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'TLM__REQ_B', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'TLM__REQ_C', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'TLM__REQ_D', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'TLM__REQ_E', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'TLM__REQ_F', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'AUX_PREORB', 'product_type_expected': 14.0, 'timeliness': '10 min'}, {'product_type': 'AUX_RESORB', 'product_type_expected': 14.0, 'timeliness': '10 min'}, {'product_type': 'AUX_POEORB', 'product_type_expected': 1.0, 'timeliness': '10 min'}]```

S2:```json[{'product_type': 'AUX_ECMWFD', 'product_type_expected': 2.0, 'timeliness': '10 min'}, {'product_type': 'AUX_CAMSFO', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'AUX_UT1UTC', 'product_type_expected': 0.14285714285714285, 'timeliness': '30 min'}, {'product_type': 'TLM__REQ_A', 'product_type_expected': 6.0, 'timeliness': '30 min'}, {'product_type': 'TLM__REQ_B', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'REP__CHF__', 'product_type_expected': 0.14285714285714285, 'timeliness': '30 min'}, {'product_type': 'REP__FCHF__', 'product_type_expected': 0.14285714285714285, 'timeliness': '30 min'}, {'product_type': 'MPL_ORBPRE', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'MPL_ORBRES', 'product_type_expected': 1.0, 'timeliness': '30 min'}]```

S3:```json[{'product_type': 'AX___MF1_AX', 'product_type_expected': 8.0, 'timeliness': '10 min'}, {'product_type': 'AX___MFA_AX', 'product_type_expected': 4.0, 'timeliness': '10 min'}, {'product_type': 'AX___MA1_AX', 'product_type_expected': 4.0, 'timeliness': '10 min'}, {'product_type': 'AX___MF2_AX', 'product_type_expected': 8.0, 'timeliness': '10 min'}, {'product_type': 'AX___MA2_AX', 'product_type_expected': 4.0, 'timeliness': '10 min'}, {'product_type': 'SR___MDO_AX', 'product_type_expected': 2.0, 'timeliness': '10 min'}, {'product_type': 'SR_2_PMPSAX', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'SR_2_RMO_AX', 'product_type_expected': 4.0, 'timeliness': '10 min'}, {'product_type': 'SR_2_PMO_AX', 'product_type_expected': 4.0, 'timeliness': '10 min'}, {'product_type': 'SR_2_POL_AX', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'SR_2_PGI_AX', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'SR_2_RGI_AX', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'SR_1_USO_AX', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'SR___MGNSAX', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'SL_2_SSTAAX', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'SL_2_DIMSAX', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'AX___FPO_AX', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'AX___FRO_AX', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'SR_2_PCPPAX', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'SR_2_PMPPAX', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'SR___MGNPAX', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'SR___POEPAX', 'product_type_expected': 2.0, 'timeliness': '30 min'}, {'product_type': 'SR_2_SIFNAX', 'product_type_expected': 1.0, 'timeliness': '30 min'}, {'product_type': 'SR_2_SIFSAX', 'product_type_expected': 1.0, 'timeliness': '30 min'}]```



Time reference for this dashboard is : publication_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## AUXIP-LTA Completeness[🔗](https://omcs.copernicus.eu/grafana/d/MxhCdfbnz/auxip-lta-completeness)

**Section**: Completeness

**Description**: 

This dashboard features a comparison between product published at the following interfaces:
 - AUXIP;
 - LTA.

Discrepancies are displayed through the following indicators:
 - Total missing product count;
 - Missed products over time;
 - Pie chart view of product status;
 - Detailed list of missing products.

Information is available for each mission and each LTA managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Mission and LTA service to consider can be selected in the upper bar.


Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## AUXIP-MPCIP Completeness[🔗](https://omcs.copernicus.eu/grafana/d/ae161631-ec00-4999-a942-b601956d6998/auxip-mpcip-completeness)

**Section**: Completeness

**Description**: 

This dashboard features a comparison between product published at the following interfaces:
 - AUXIP
 - MPCIP

Discrepancies are displayed through the following indicators:
 - Total missing product count;
 - Missed products over time;
 - Pie chart view of product status;
 - Detailed list of missing products.

Information is available for each mission and each AUXIP/MPCIP managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Mission and LTA service to consider can be selected in the upper bar.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## DD Completeness[🔗](https://omcs.copernicus.eu/grafana/d/yDEHKjS4k/dd-completeness)

**Section**: Completeness

**Description**: 

This dashboard features a comparison between product published at the following interfaces:
 - PRIP
 - AUXIP
 - DD DHUS, DAS.

Discrepancies are displayed through the following indicators:
 - Total missing product count;
 - Missed products over time;
 - Pie chart view of product status;
 - Detailed list of missing products.

Information is available for each mission and each PRIP managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Mission service to consider can be selected in the upper bar.
 - Dissemination service to consider can be selected in the upper bar filter named "Dissemination service" ddip is DD_DHUS, dddas is DD_DAS.

 This Dashboard use the [Copernicus Ground Segment Sentinels Data Flow Configuration V1.2](/grafana/d/MfmL_E4Vz/dataflow-configuration?orgId=1) as reference


Note : Some product category are not disseminated to DHUS :

CDSE started to ingest the S-1 and S-3 engineering data from 12.09.2023 10:00 CEST in order to avoid misunderstanding on the completeness.
https://esa-cams.atlassian.net/browse/PDGSMNT-3234

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## LTA Completeness[🔗](https://omcs.copernicus.eu/grafana/d/KnP3Me7Vk/lta-completeness)

**Section**: Completeness

**Description**: 

This dashboard features a comparison between product published at the following interfaces:
 - AUXIP;
 - LTA.

Discrepancies are displayed through the following indicators:
 - Total missing product count;
 - Missed products over time;
 - Pie chart view of product status;
 - Detailed list of missing products.

Information is available for each mission and each LTA managed by OMCS.

For S5P Satellite, L1 & L2 products are only archived to DLR and not to CloudFerro LTA

Tips:
 - Annotations are available on time series;
 - Mission and LTA service to consider can be selected in the upper bar.

This Dashboard use the [Copernicus Ground Segment Sentinels Data Flow Configuration V1.2](/grafana/d/MfmL_E4Vz/dataflow-configuration?orgId=1) as reference

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## PRIP-DD Completeness (product count)[🔗](https://omcs.copernicus.eu/grafana/d/YfrPYWsnk/prip-dd-completeness-product-count)

**Section**: Completeness

**Description**: 

This dashboard compares products Disseminated at the DHUS with against Products Published at PRIP.


Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## PRIP-DD Completeness[🔗](https://omcs.copernicus.eu/grafana/d/ODRp3_Q7k/prip-dd-completeness)

**Section**: Completeness

**Description**: 

This dashboard features a comparison between product published at the following interfaces:
 - PRIP;
 - DD DHUS.

Discrepancies are displayed through the following indicators:
 - Total missing product count;
 - Missed products over time;
 - Pie chart view of product status;
 - Detailed list of missing products.

Information is available for each mission and each PRIP managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Mission service to consider can be selected in the upper bar.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## PRIP-LTA Completeness (All LTA)[🔗](https://omcs.copernicus.eu/grafana/d/jCljKui4z/prip-lta-completeness-all-lta)

**Section**: Completeness

**Description**: 

This dashboard features a comparison between product published at the following interfaces:
 - PRIP;
 - LTA.

Discrepancies are displayed through the following indicators:
 - Total missing product count;
 - Missed products over time;
 - Pie chart view of product status;
 - Detailed list of missing products.

Information is available for each mission and each PRIP/LTA managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Mission to consider can be selected in the upper bar.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## PRIP-LTA Completeness[🔗](https://omcs.copernicus.eu/grafana/d/XxhCdfanz/prip-lta-completeness)

**Section**: Completeness

**Description**: 

This dashboard features a comparison between product published at the following interfaces:
 - PRIP;
 - LTA.

Discrepancies are displayed through the following indicators:
 - Total missing product count;
 - Missed products over time;
 - Pie chart view of product status;
 - Detailed list of missing products.

Information is available for each mission and each PRIP/LTA managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Mission and LTA service to consider can be selected in the upper bar.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S1 Datatake Completeness (Produced vs Planned)[🔗](https://omcs.copernicus.eu/grafana/d/sStGi_ynz/s1-datatake-completeness-produced-vs-planned)

**Section**: Completeness

**Description**: 

This dashboard features Completeness computation on a single datatake of S1 mission.

Comparison is done between the following:
 - Mission Planning (MP): Planned products;
 - PRIP: Produced products.

L1_SLC and L2_OCN expected products are determined with intersection of footprints taken from RAW_0S.

L0 products expected duration are based on L0 sensing duration taken from MP.
L1/L2 products expected duration are based on Observation Duration taken from MP (except for RF_RAW__0S products that have an expected duration of 2.8s).

Tips:
 - Best approach is to start in Production Completeness dashboard and select one datatake to explore from there;
 - Satellite to consider can be selected in the upper bar.

Time reference for this dashboard is : observation_time_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S1 Production Completeness (Produced vs Planned)[🔗](https://omcs.copernicus.eu/grafana/d/9_6v0ss7z/s1-production-completeness-produced-vs-planned)

**Section**: Completeness

**Description**: 

This dashboard features Completeness computation on S1 mission.

Comparison is done between the following:
 - Mission Planning (MP): Planned products;
 - PRIP: Produced products.

L1_SLC and L2_OCN expected products are determined with intersection of footprints taken from RAW_0S.

L0 products expected duration are based on L0 sensing duration taken from MP.
L1/L2 products expected duration are based on Observation Duration taken from MP (except for RF_RAW__0S products that have an expected duration of 2.8s).

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.

Time reference for this dashboard is : observation_time_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S2 Datatake Completeness (Produced vs Planned)[🔗](https://omcs.copernicus.eu/grafana/d/sStGi_ymz/s2-datatake-completeness-produced-vs-planned)

**Section**: Completeness

**Description**: 

This dashboard features Completeness computation on a single datatake of S2 mission.

Comparison is done between the following:
 - Mission Planning (MP): Planned products;
 - PRIP: Produced products.

TL / TC expected products are determined by intersection of footprints taken from MSI_L1C_DS.

Expected Granules (MSI_L0__GR) are based on the number of scene of the level multiplied per 12. (TODO: use MSI_??_DS).

L0_DS products expected duration are based on Observation Duration taken from MP.
L1B_DS, L1C_DS and L2A products expected duration are based on Observation Duration of MP minus 2*3,608s (duration of one scene).

Finally, if scene count is inferior to 3, L0 products are the only ones expected.

Tips:
 - Best approach is to start in Production Completeness dashboard and select one datatake to explore from there;
 - Satellite to consider can be selected in the upper bar.

Time reference for this dashboard is : observation_time_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S2 Production Completeness (Produced vs Planned)[🔗](https://omcs.copernicus.eu/grafana/d/9_6v0ss8z/s2-production-completeness-produced-vs-planned)

**Section**: Completeness

**Description**: 

This dashboard features Completeness computation on S2 mission.

Comparison is done between the following:
 - Mission Planning (MP): Planned products;
 - PRIP: Produced products.

TL / TC expected products are determined by intersection of footprints taken from MSI_L1C_DS.

Expected Granules (MSI_L0__GR) are based on the number of scene of the level multiplied per 12. (TODO: use MSI_??_DS).

L0_DS products expected duration are based on Observation Duration taken from MP.
L1B_DS, L1C_DS and L2A products expected duration are based on Observation Duration of MP minus 2*3,608s (duration of one scene).

Finally, if scene count is inferior to 3, L0 products are the only ones expected.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.

Time reference for this dashboard is : observation_time_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S3 Datatake Completeness (Produced vs Planned)[🔗](https://omcs.copernicus.eu/grafana/d/tStGj_ynz/s3-datatake-completeness-produced-vs-planned)

**Section**: Completeness

**Description**: 

This dashboard features Completeness computation on a single datatake of S3 mission.

Comparison is done using the following:
 - PRIP: Produced products.

Datatake ID are built from:
 - Satellite number;
 - Cycle number;
 - Relative orbit number.

When one PRIP product is published, every expected product related to this datatake is created.

Missing products are displayed in purple.

Tips:
 - Best approach is to start in Production Completeness dashboard and select one datatake to explore from there;
 - Satellite to consider can be selected in the upper bar (has to be the same as the datatake ID prefix).

Note: 
 - SRAL L2, VG1 and V10 products are not included in the completeness computation since these products are not systematically produced at each orbit (production is not predictable).


Time reference for this dashboard is : observation_time_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S3 Production Completeness (Produced vs Planned)[🔗](https://omcs.copernicus.eu/grafana/d/T_6v1ss8z/s3-production-completeness-produced-vs-planned)

**Section**: Completeness

**Description**: 

This dashboard features Completeness computation on S3 mission.

Comparison is done using the following:
 - PRIP: Produced products.

Datatake ID are built from:
 - Satellite number;
 - Cycle number;
 - Relative orbit number.

When one PRIP product is published, every expected product related to this datatake is created.

Missing products are displayed in purple.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.

Note: 
 - SRAL L2, VG1 and V10 products are not included in the completeness computation since these products are not systematically produced at each orbit (production is not predictable).


Time reference for this dashboard is : observation_time_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S5 Datatake Completeness (Produced vs Planned)[🔗](https://omcs.copernicus.eu/grafana/d/3lDUD2gVz/s5-datatake-completeness-produced-vs-planned)

**Section**: Completeness

**Description**: 

This dashboard features Completeness computation on a single datatake of S5 mission.

Comparison is done using the following:
 - PRIP: Produced products.

Datatake ID are built from:
 - Satellite number;
 - Absolute orbit number.

When one PRIP product is published, every expected product related to this datatake is created.

Missing products are displayed in purple.

Tips:
 - Best approach is to start in Production Completeness dashboard and select one datatake to explore from there;
 - Satellite to consider can be selected in the upper bar (has to be the same as the datatake ID prefix).

Time reference for this dashboard is : observation_time_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S5 Production Completeness (Produced vs Planned)[🔗](https://omcs.copernicus.eu/grafana/d/eI1yShRVz/s5-production-completeness-produced-vs-planned)

**Section**: Completeness

**Description**: 

This dashboard features Completeness computation on S5 mission.

Comparison is done using the following:
 - PRIP: Produced products.

Datatake ID are built from:
 - Satellite number;
 - Absolute orbit number.

When one PRIP product is published, every expected product related to this datatake is created.

Missing products are displayed in purple.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.

Time reference for this dashboard is : observation_time_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## DD Completeness (Manual Parameter Selection)[🔗](https://omcs.copernicus.eu/grafana/d/d9690bb2-f8fb-4b79-98a8-6b01426bf17b/dd-completeness-manual-parameter-selection)

**Section**: Debug

**Description**: 

This dashboard features a comparison between product published at the following interfaces:
 - PRIP;
 - DD DHUS, DAS.

Discrepancies are displayed through the following indicators:
 - Total missing product count;
 - Missed products over time;
 - Pie chart view of product status;
 - Detailed list of missing products.

Information is available for each mission and each PRIP managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Mission service to consider can be selected in the upper bar.
 - Dissemination service to consider can be selected in the upper bar filter named "Dissemination service" ddip is DD_DHUS, dddas is DD_DAS.

 This Dashboard use the [Copernicus Ground Segment Sentinels Data Flow Configuration V1.2](/grafana/d/MfmL_E4Vz/dataflow-configuration?orgId=1) as reference


Note : Some product category are not disseminated to DHUS :


Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Product Inventory - Origin Date[🔗](https://omcs.copernicus.eu/grafana/d/bbf187f7-7fcf-4000-b225-738cb7b88ffc/product-inventory-origin-date)

**Section**: Debug

**Description**: 

This dashboard features information on:

Detailed list of origin dates for a specific product from Product Inventory Dashboard
Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Interface monitoring Global view[🔗](https://omcs.copernicus.eu/grafana/d/F58sJjg4k/interface-monitoring-global-view)

**Section**: Interface_Monitoring

**Description**: 

This dashboard features an overview of the interfaces managed by OMCS.

Status is displayed with the following indicators:
 - A dashboard of interface with its status (green: OK, red: FAILED);
 - A detailed list of interface unavailability;
 - Timeline of interface status.

Each interface is monitored through a periodic availability check.

Time reference for this dashboard is : probe_time_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## System Technical Budget Diagrams[🔗](https://omcs.copernicus.eu/grafana/d/6EM0vcK4z/system-technical-budget-diagrams)

**Section**: STB

**Description**: 

The System Technical Budget Diagrams is based on 



- the data budget reference document [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2).



- the data flow reference document [\[ESA-EOPG-EOPGC-TN-58\] CSC GS Data Flow Configuration.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-58%5D%20CSC%20GS%20Data%20Flow%20Configuration.pdf?api=v2).



Data flow document extraction is visible in the ["Data Flow dashboard"](./d/MfmL_E4Vz/golden-rules-and-data-flow?orgId=1) 



### Data selected



From [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2) document some assuption are made to provide the System Technical Budget dashboards.



For System Technical Budget Diagrams the data published at PRIP, LTA or DD and DSIB files are selected.



 - Section Data Aquisition data from DSIB files.

 - Section Data Production data published at PRIP.

 - Section Data Preservation data published at LTA.

 - Section Data Distribution data published at DD.



**Data collection** are considered as consistent since **01/08/2022**

**Data collection** for **aquisition** are considered as consistent since **15/03/2023**



Values are mean by satellite number in mission. (i.e. S1 1 satellite, S2 mean of 2 satellite, S3 mean of 2 satellite; S5 1 satellite )



For S1, S2, S3 values are mean of the 4 LTA, for S5 values came from S5P_DLR.



Rmq : There is today no S5 L0 data published at prip.



### Annexes



#### Product type selected



The tables below present how products types are classified in STB level and STB timeliness:



##### For panel **Yearly downlinked data volume (TiB)**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|




##### For panel **Yearly downlinked data number**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|




##### For panel **Yearly NTC Production volume of products (L1 & L2) S1, S3, S5P and S2 (TiB)**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|||NTC|2022|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_SLC__1A, IW_SLC__1S, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_SLC__1A, WV_SLC__1S|
|S2|||NOMINAL|2022|MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S3|||NT|2022|MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___|
|S5|||OFFL|2022|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S1|||NTC|2023|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_SLC__1A, IW_SLC__1S, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_SLC__1A, WV_SLC__1S|
|S2|||NOMINAL|2023|MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S3|||NT|2023|MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___|
|S5|||OFFL|2023|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|




##### For panel **Yearly NTC Production number of products (L1 & L2) S1, S3, S5P and S2**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|||NTC|2022|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_SLC__1A, IW_SLC__1S, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_SLC__1A, WV_SLC__1S|
|S2|||NOMINAL|2022|MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S3|||NT|2022|MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___|
|S5|||OFFL|2022|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S1|||NTC|2023|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_SLC__1A, IW_SLC__1S, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_SLC__1A, WV_SLC__1S|
|S2|||NOMINAL|2023|MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S3|||NT|2023|MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___|
|S5|||OFFL|2023|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|




##### For panel **Yearly NRT Production volume of products (L1 & L2) S1, S3, S5P (TiB)**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|||NRT,NRT-PT|2022|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_SLC__1A, IW_SLC__1S|
|S3|||NR,AL|2022|MW_1_CAL___, MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_1_RBT___, SL_2_LST___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___|
|S3|||ST|2022|MW_1_MWR___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S3|||NT|2022|SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S5|||NRTI|2022|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S1|||NRT,NRT-PT|2023|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_SLC__1A, IW_SLC__1S|
|S3|||NR,AL|2023|MW_1_CAL___, MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_1_RBT___, SL_2_LST___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___|
|S3|||ST|2023|MW_1_MWR___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S3|||NT|2023|SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S5|||NRTI|2023|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|




##### For panel **Yearly NRT Production number of products (L1 & L2) S1, S3, S5P**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|||NRT,NRT-PT|2022|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_SLC__1A, IW_SLC__1S|
|S3|||NR,AL|2022|MW_1_CAL___, MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_1_RBT___, SL_2_LST___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___|
|S3|||ST|2022|MW_1_MWR___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S3|||NT|2022|SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S5|||NRTI|2022|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S1|||NRT,NRT-PT|2023|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_SLC__1A, IW_SLC__1S|
|S3|||NR,AL|2023|MW_1_CAL___, MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_1_RBT___, SL_2_LST___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___|
|S3|||ST|2023|MW_1_MWR___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S3|||NT|2023|SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S5|||NRTI|2023|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|




##### For panel **Yearly NTC Production volume of products S1, S3, S5P (TiB)**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|||NTC|2022|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S3|||NT|2022|MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___|
|S5|||OFFL|2022|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|2022|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S1|||NTC|2023|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S3|||NT|2023|MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___|
|S5|||OFFL|2023|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|2023|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|




##### For panel **Yearly NTC Production number of products S1, S3, S5P**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|||NTC|2022|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S3|||NT|2022|MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___|
|S5|||OFFL|2022|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|2022|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S1|||NTC|2023|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S3|||NT|2023|MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___|
|S5|||OFFL|2023|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|2023|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|




##### For panel **Yearly NTC Production volume of products S2 (TiB)**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S2|||NOMINAL|2022|MSI_L0__DS, MSI_L0__GR, MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|||NOMINAL|2023|MSI_L0__DS, MSI_L0__GR, MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|




##### For panel **Yearly NTC Production number of products S2**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S2|||NOMINAL|2022|MSI_L0__DS, MSI_L0__GR, MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|||NOMINAL|2023|MSI_L0__DS, MSI_L0__GR, MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|




##### For panel **Yearly NRT Production volume of products S1, S3, S5P (TiB)**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|||NRT,NRT-PT|2022|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S3|||NR,AL|2022|DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___|
|S3|||ST|2022|MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S3|||NT|2022|SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S5|||NRTI|2022|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S1|||NRT,NRT-PT|2023|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S3|||NR,AL|2023|DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___|
|S3|||ST|2023|MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S3|||NT|2023|SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S5|||NRTI|2023|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|




##### For panel **Yearly NRT Production number of products S1, S3, S5P**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|||NRT,NRT-PT|2022|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S3|||NR,AL|2022|DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___|
|S3|||ST|2022|MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S3|||NT|2022|SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S5|||NRTI|2022|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S1|||NRT,NRT-PT|2023|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S3|||NR,AL|2023|DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___|
|S3|||ST|2023|MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S3|||NT|2023|SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S5|||NRTI|2023|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|




##### For panel **L0 Cumulative volume of products(TiB)**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|||NRT,NRT-PT|2022|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|||NTC|2022|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S2|||NOMINAL|2022|MSI_L0__DS, MSI_L0__GR|
|S3|||NR,AL|2022|DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, SL_0_SLT___, SR_0_CAL___, SR_0_SRA___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___|
|S3|||NT|2022|OL_0_EFR___, SL_0_SLT___|
|S3|||ST|2022|SR_0_SRA___|
|S5|||OPER|2022|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S1|||NRT,NRT-PT|2023|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|||NTC|2023|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S2|||NOMINAL|2023|MSI_L0__DS, MSI_L0__GR|
|S3|||NR,AL|2023|DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, SL_0_SLT___, SR_0_CAL___, SR_0_SRA___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___|
|S3|||NT|2023|OL_0_EFR___, SL_0_SLT___|
|S3|||ST|2023|SR_0_SRA___|
|S5|||OPER|2023|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|




##### For panel **L0 Cumulative number of products**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|||NRT,NRT-PT|2022|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|||NTC|2022|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S2|||NOMINAL|2022|MSI_L0__DS, MSI_L0__GR|
|S3|||NR,AL|2022|DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, SL_0_SLT___, SR_0_CAL___, SR_0_SRA___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___|
|S3|||NT|2022|OL_0_EFR___, SL_0_SLT___|
|S3|||ST|2022|SR_0_SRA___|
|S5|||OPER|2022|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S1|||NRT,NRT-PT|2023|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|||NTC|2023|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S2|||NOMINAL|2023|MSI_L0__DS, MSI_L0__GR|
|S3|||NR,AL|2023|DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, SL_0_SLT___, SR_0_CAL___, SR_0_SRA___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___|
|S3|||NT|2023|OL_0_EFR___, SL_0_SLT___|
|S3|||ST|2023|SR_0_SRA___|
|S5|||OPER|2023|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|




##### For panel **Yearly Data Distribution published volume of products S1, S3, S5 and S2 (TiB)**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|||NRT,NRT-PT|2022|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S1|||NTC|2022|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S2|||NOMINAL|2022|MSI_L0__DS, MSI_L0__GR, MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S3|||NR,AL|2022|DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___|
|S3|||NT|2022|MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S3|||ST|2022|MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S5|||NRTI|2022|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|||OFFL|2022|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|2022|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S1|||NRT,NRT-PT|2023|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S1|||NTC|2023|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S2|||NOMINAL|2023|MSI_L0__DS, MSI_L0__GR, MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S3|||NR,AL|2023|DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___|
|S3|||NT|2023|MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S3|||ST|2023|MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S5|||NRTI|2023|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|||OFFL|2023|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|2023|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|




##### For panel **Yearly Data Distribution published number of products S1, S3, S5 and S2 (TiB)**:



@Yearly Data Distribution published number of products S1, S3, S5 and S2 (TiB)@







### Dashboard usage



On left top of the dashboard the mean combobox allow to select mean period:



- none: values for the selected period.

- by day: values are divided by the number of seconds in the selected periode divided by the number of seconds in 1 day.

- by week: values are divided by the number of seconds in the selected periode divided by the number of seconds in 7 day.

- by month: values are divided by the number of seconds in the selected periode divided by the number of seconds in 30 day.

- by year: values are divided by the number of seconds in the selected periode divided by the number of seconds in 365 day.


Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## System Technical Budget Schematic View - S1[🔗](https://omcs.copernicus.eu/grafana/d/N9YlQDKVk/system-technical-budget-schematic-view-s1)

**Section**: STB

**Description**: 

The System Technical Budget Schematic View - S1 is based on 



- the data budget reference document [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2).



- the data flow reference document [\[ESA-EOPG-EOPGC-TN-58\] CSC GS Data Flow Configuration.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-58%5D%20CSC%20GS%20Data%20Flow%20Configuration.pdf?api=v2).



Data flow document extraction is visible in the ["Data Flow dashboard"](./d/MfmL_E4Vz/golden-rules-and-data-flow?orgId=1) 



### Data selected



From [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2) document some assuption are made to provide the System Technical Budget dashboards.



For System Technical Budget Schematic View - S1 the data published at PRIP, LTA or DD and DSIB files are selected.



 - Section Data Aquisition data from DSIB files.

 - Section Data Production data published at PRIP.

 - Section Data Preservation data published at LTA.

 - Section Data Distribution data published at DD.



**Data collection** are considered as consistent since **01/08/2022**

**Data collection** for **aquisition** are considered as consistent since **15/03/2023**



Values are mean by satellite number in mission. (i.e. S1 1 satellite, S2 mean of 2 satellite, S3 mean of 2 satellite; S5 1 satellite )



For S1, S2, S3 values are mean of the 4 LTA, for S5 values came from S5P_DLR.



Rmq : There is today no S5 L0 data published at prip.



### Annexes



#### Product type selected



The tables below present how products types are classified in STB level and STB timeliness:



##### For panel **Yearly Overall Data Flow S1 SATELLITE**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|||NRT,NRT-PT|ACQ VOL|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S1|||NTC|ACQ VOL|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S1|||NRT,NRT-PT|ACQ COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S1|||NTC|ACQ COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S1|L0|NRT|NRT,NRT-PT|PROD VOL|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|L0|NRT|NRT,NRT-PT|PROD COUNT|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|L1|NRT|NRT,NRT-PT|PROD VOL|EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S|
|S1|L1|NRT|NRT,NRT-PT|PROD COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S|
|S1|L0|NTC|NTC|PROD VOL|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S1|L0|NTC|NTC|PROD COUNT|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S1|L1|NTC|NTC|PROD VOL|EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S, S1_GRDH_1A, S1_GRDH_1S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_SLC__1A, S6_SLC__1S, WV_SLC__1A, WV_SLC__1S|
|S1|L1|NTC|NTC|PROD COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S, S1_GRDH_1A, S1_GRDH_1S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_SLC__1A, S6_SLC__1S, WV_SLC__1A, WV_SLC__1S|
|S1|L2|NRT|NRT,NRT-PT|PROD VOL|EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S|
|S1|L2|NRT|NRT,NRT-PT|PROD COUNT|EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S|
|S1|L2|NTC|NTC|PROD VOL|EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S, S1_OCN__2A, S1_OCN__2S, S2_OCN__2A, S2_OCN__2S, S3_OCN__2A, S3_OCN__2S, S4_OCN__2A, S4_OCN__2S, S5_OCN__2A, S5_OCN__2S, S6_OCN__2A, S6_OCN__2S, WV_OCN__2A, WV_OCN__2S|
|S1|L2|NTC|NTC|PROD COUNT|EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S, S1_OCN__2A, S1_OCN__2S, S2_OCN__2A, S2_OCN__2S, S3_OCN__2A, S3_OCN__2S, S4_OCN__2A, S4_OCN__2S, S5_OCN__2A, S5_OCN__2S, S6_OCN__2A, S6_OCN__2S, WV_OCN__2A, WV_OCN__2S|
|S1||NRT-NTC|NRT,NRT-PT|PROD TOT VOL|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S1||NRT-NTC|NTC|PROD TOT VOL|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S1||NRT-NTC|NRT,NRT-PT|PROD TOT COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S1||NRT-NTC|NTC|PROD TOT COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S1|L0|NRT-NTC|NRT,NRT-PT|LTA VOL|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|L0|NRT-NTC|NTC|LTA VOL|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S1|L0|NRT-NTC|NRT,NRT-PT|LTA COUNT|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|L0|NRT-NTC|NTC|LTA COUNT|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S1|L0|NRT-NTC|NRT,NRT-PT|DD VOL|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|L0|NRT-NTC|NTC|DD VOL|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S1|L0|NRT-NTC|NRT,NRT-PT|DD COUNT|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|L0|NRT-NTC|NTC|DD COUNT|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S1|L1|NRT-NTC|NRT,NRT-PT|DD VOL|EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S|
|S1|L1|NRT-NTC|NTC|DD VOL|EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S, S1_GRDH_1A, S1_GRDH_1S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_SLC__1A, S6_SLC__1S, WV_SLC__1A, WV_SLC__1S|
|S1|L1|NRT-NTC|NRT,NRT-PT|DD COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S|
|S1|L1|NRT-NTC|NTC|DD COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S, S1_GRDH_1A, S1_GRDH_1S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_SLC__1A, S6_SLC__1S, WV_SLC__1A, WV_SLC__1S|
|S1|L2|NRT-NTC|NRT,NRT-PT|DD VOL|EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S|
|S1|L2|NRT-NTC|NTC|DD VOL|EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S, S1_OCN__2A, S1_OCN__2S, S2_OCN__2A, S2_OCN__2S, S3_OCN__2A, S3_OCN__2S, S4_OCN__2A, S4_OCN__2S, S5_OCN__2A, S5_OCN__2S, S6_OCN__2A, S6_OCN__2S, WV_OCN__2A, WV_OCN__2S|
|S1|L2|NRT-NTC|NRT,NRT-PT|DD COUNT|EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S|
|S1|L2|NRT-NTC|NTC|DD COUNT|EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S, S1_OCN__2A, S1_OCN__2S, S2_OCN__2A, S2_OCN__2S, S3_OCN__2A, S3_OCN__2S, S4_OCN__2A, S4_OCN__2S, S5_OCN__2A, S5_OCN__2S, S6_OCN__2A, S6_OCN__2S, WV_OCN__2A, WV_OCN__2S|
|S1||NRT-NTC|NRT,NRT-PT|DD TOT VOL|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S1||NRT-NTC|NTC|DD TOT VOL|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S1||NRT-NTC|NRT,NRT-PT|DD TOT COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S1||NRT-NTC|NTC|DD TOT COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S1|L0|NRT-NTC|NRT,NRT-PT|DL VOL|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|L0|NRT-NTC|NTC|DL VOL|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S1|L0|NRT-NTC|NRT,NRT-PT|DL COUNT|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|L0|NRT-NTC|NTC|DL COUNT|EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S1|L1|NRT-NTC|NRT,NRT-PT|DL VOL|EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S|
|S1|L1|NRT-NTC|NTC|DL VOL|EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S, S1_GRDH_1A, S1_GRDH_1S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_SLC__1A, S6_SLC__1S, WV_SLC__1A, WV_SLC__1S|
|S1|L1|NRT-NTC|NRT,NRT-PT|DL COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S|
|S1|L1|NRT-NTC|NTC|DL COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S, S1_GRDH_1A, S1_GRDH_1S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_SLC__1A, S6_SLC__1S, WV_SLC__1A, WV_SLC__1S|
|S1|L2|NRT-NTC|NRT,NRT-PT|DL VOL|EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S|
|S1|L2|NRT-NTC|NTC|DL VOL|EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S, S1_OCN__2A, S1_OCN__2S, S2_OCN__2A, S2_OCN__2S, S3_OCN__2A, S3_OCN__2S, S4_OCN__2A, S4_OCN__2S, S5_OCN__2A, S5_OCN__2S, S6_OCN__2A, S6_OCN__2S, WV_OCN__2A, WV_OCN__2S|
|S1|L2|NRT-NTC|NRT,NRT-PT|DL COUNT|EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S|
|S1|L2|NRT-NTC|NTC|DL COUNT|EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S, S1_OCN__2A, S1_OCN__2S, S2_OCN__2A, S2_OCN__2S, S3_OCN__2A, S3_OCN__2S, S4_OCN__2A, S4_OCN__2S, S5_OCN__2A, S5_OCN__2S, S6_OCN__2A, S6_OCN__2S, WV_OCN__2A, WV_OCN__2S|
|S1||NRT-NTC|NRT,NRT-PT|DL TOT VOL|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S1||NRT-NTC|NTC|DL TOT VOL|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|
|S1||NRT-NTC|NRT,NRT-PT|DL TOT COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S|
|S1||NRT-NTC|NTC|DL TOT COUNT|EW_GRDM_1A, EW_GRDM_1S, EW_OCN__2A, EW_OCN__2S, EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_OCN__2A, IW_OCN__2S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, IW_SLC__1A, IW_SLC__1S, RF_RAW, S1_GRDH_1A, S1_GRDH_1S, S1_OCN__2A, S1_OCN__2S, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_OCN__2A, S2_OCN__2S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_OCN__2A, S3_OCN__2S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_OCN__2A, S4_OCN__2S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_OCN__2A, S5_OCN__2S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_OCN__2A, S6_OCN__2S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, S6_SLC__1A, S6_SLC__1S, WV_OCN__2A, WV_OCN__2S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S, WV_SLC__1A, WV_SLC__1S|



Time reference fot this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## System Technical Budget Schematic View - S2[🔗](https://omcs.copernicus.eu/grafana/d/SIMuwDKVz/system-technical-budget-schematic-view-s2)

**Section**: STB

**Description**: 

The System Technical Budget Schematic View - S2 is based on 



- the data budget reference document [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2).



- the data flow reference document [\[ESA-EOPG-EOPGC-TN-58\] CSC GS Data Flow Configuration.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-58%5D%20CSC%20GS%20Data%20Flow%20Configuration.pdf?api=v2).



Data flow document extraction is visible in the ["Data Flow dashboard"](./d/MfmL_E4Vz/golden-rules-and-data-flow?orgId=1) 



### Data selected



From [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2) document some assuption are made to provide the System Technical Budget dashboards.



For System Technical Budget Schematic View - S2 the data published at PRIP, LTA or DD and DSIB files are selected.



 - Section Data Aquisition data from DSIB files.

 - Section Data Production data published at PRIP.

 - Section Data Preservation data published at LTA.

 - Section Data Distribution data published at DD.



**Data collection** are considered as consistent since **01/08/2022**

**Data collection** for **aquisition** are considered as consistent since **15/03/2023**



Values are mean by satellite number in mission. (i.e. S1 1 satellite, S2 mean of 2 satellite, S3 mean of 2 satellite; S5 1 satellite )



For S1, S2, S3 values are mean of the 4 LTA, for S5 values came from S5P_DLR.



Rmq : There is today no S5 L0 data published at prip.



### Annexes



#### Product type selected



The tables below present how products types are classified in STB level and STB timeliness:



##### For panel **Yearly Overall Data Flow S2 SATELLITE**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S2|||NOMINAL|ACQ VOL|MSI_L0__DS, MSI_L0__GR, MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|||NOMINAL|ACQ COUNT|MSI_L0__DS, MSI_L0__GR, MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|L0||NOMINAL|PROD VOL|MSI_L0__DS, MSI_L0__GR|
|S2|L0||NOMINAL|PROD COUNT|MSI_L0__DS, MSI_L0__GR|
|S2|L1C||NOMINAL|PROD VOL|MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL|
|S2|L1C||NOMINAL|PROD COUNT|MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL|
|S2|L1B||NOMINAL|PROD VOL|MSI_L1B_DS, MSI_L1B_GR|
|S2|L1B||NOMINAL|PROD COUNT|MSI_L1B_DS, MSI_L1B_GR|
|S2|L2A||NOMINAL|PROD VOL|MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|L2A||NOMINAL|PROD COUNT|MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|||NOMINAL|PROD TOT VOL|MSI_L0__DS, MSI_L0__GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|||NOMINAL|PROD TOT COUNT|MSI_L0__DS, MSI_L0__GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|L0||NOMINAL|LTA VOL|MSI_L0__DS, MSI_L0__GR|
|S2|L0||NOMINAL|LTA COUNT|MSI_L0__DS, MSI_L0__GR|
|S2|L1C||NOMINAL|DD VOL|MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL|
|S2|L1C||NOMINAL|DD COUNT|MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL|
|S2|L2A||NOMINAL|DD VOL|MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|L2A||NOMINAL|DD COUNT|MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|||NOMINAL|DD TOT VOL|MSI_L0__DS, MSI_L0__GR, MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|||NOMINAL|DD TOT COUNT|MSI_L0__DS, MSI_L0__GR, MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|L1||NOMINAL|DL VOL|MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL|
|S2|L1||NOMINAL|DL COUNT|MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL|
|S2|L2||NOMINAL|DL VOL|MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|L2||NOMINAL|DL COUNT|MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|||NOMINAL|DL TOT VOL|MSI_L0__DS, MSI_L0__GR, MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S2|||NOMINAL|DL TOT COUNT|MSI_L0__DS, MSI_L0__GR, MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___ , MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL, MSI_L2A___ , MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|


Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## System Technical Budget Schematic View - S3[🔗](https://omcs.copernicus.eu/grafana/d/-sLXQDFVk/system-technical-budget-schematic-view-s3)

**Section**: STB

**Description**: 

The System Technical Budget Schematic View - S3 is based on
- the data budget reference document [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2).
- the data flow reference document [\[ESA-EOPG-EOPGC-TN-58\] CSC GS Data Flow Configuration.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-58%5D%20CSC%20GS%20Data%20Flow%20Configuration.pdf?api=v2).

Data flow document extraction is visible in the ["Data Flow dashboard"](./d/MfmL_E4Vz/golden-rules-and-data-flow?orgId=1) 

### Data selected

From [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2) document some assuption are made to provide the System Technical Budget dashboards.

For System Technical Budget Schematic View - S3 the data published at PRIP, LTA or DD and DSIB files are selected.
- Section Data Aquisition data from DSIB files.
- Section Data Production data published at PRIP.
- Section Data Preservation data published at LTA.
- Section Data Distribution data published at DD.

**Data collection** are considered as consistent since **01/08/2022**

**Data collection** for **aquisition** are considered as consistent since **15/03/2023**

Values are mean by satellite number in mission. ( i.e. S1 1 satellite, S2 mean of 2 satellite, S3 mean of 2 satellite; S5 1 satellite )

For S1, S2, S3 values are mean of the 4 LTA, for S5 values came from S5P_DLR.

Rmq: There is today no S5 L0 data published at prip.
### Annexes

#### Product type selected

The tables below present how products types are classified in STB level and STB timeliness:

##### For panel **Yearly Overall Data Flow S3 SATELLITE**:

| Mission | STB Level | STB Timeliness | Real timeliness | Misc.          | Product Type                                                                                                                                                                                                                                                                                                                                     |
| ------- | --------- | -------------- | --------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| S3      |           |                | NR, AL          | ACQ VOL        | DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___ |
| S3      |           |                | NT              | ACQ VOL        | MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                  |
| S3      |           |                | ST              | ACQ VOL        | MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                       |
| S3      |           |                | NR, AL          | ACQ COUNT      | DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___ |
| S3      |           |                | NT              | ACQ COUNT      | MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                  |
| S3      |           |                | ST              | ACQ COUNT      | MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                       |
| S3      | L0        | NRT            | NR, AL          | PROD STC VOL   | DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, SL_0_SLT___, SR_0_CAL___, SR_0_SRA___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___                                                                                                                                                                          |
| S3      | L0        | NRT            | ST              | PROD STC VOL   | SR_0_SRA___                                                                                                                                                                                                                                                                                                                                      |
| S3      | L0        | NRT            | NR, AL          | PROD STC COUNT | DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, SL_0_SLT___, SR_0_CAL___, SR_0_SRA___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___                                                                                                                                                                          |
| S3      | L0        | NRT            | ST              | PROD STC COUNT | SR_0_SRA___                                                                                                                                                                                                                                                                                                                                      |
| S3      | L0        | NTC            | NT              | PROD VOL       | OL_0_EFR___, SL_0_SLT___                                                                                                                                                                                                                                                                                                                         |
| S3      | L0        | NTC            | NT              | PROD COUNT     | OL_0_EFR___, SL_0_SLT___                                                                                                                                                                                                                                                                                                                         |
| S3      | L1        | NRT            | NR, AL          | PROD STC VOL   | MW_1_CAL___, MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, SL_1_RBT___, SR_1_CAL___, SR_1_SRA___                                                                                                                                                                                                                              |
| S3      | L1        | NRT            | ST              | PROD STC VOL   | MW_1_MWR___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__                                                                                                                                                                                                                                                                                  |
| S3      | L1        | NRT            | NR, AL          | PROD STC COUNT | MW_1_CAL___, MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, SL_1_RBT___, SR_1_CAL___, SR_1_SRA___                                                                                                                                                                                                                              |
| S3      | L1        | NRT            | ST              | PROD STC COUNT | MW_1_MWR___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__                                                                                                                                                                                                                                                                                  |
| S3      | L2        | NRT            | NR, AL          | PROD STC VOL   | OL_2_LFR___, OL_2_LRR___, SL_2_LST___, SR_2_LAN___                                                                                                                                                                                                                                                                                               |
| S3      | L2        | NRT            | ST              | PROD STC VOL   | SR_2_LAN___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                                                                                                     |
| S3      | L2        | NRT            | NR, AL          | PROD STC COUNT | OL_2_LFR___, OL_2_LRR___, SL_2_LST___, SR_2_LAN___                                                                                                                                                                                                                                                                                               |
| S3      | L2        | NRT            | ST              | PROD STC COUNT | SR_2_LAN___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                                                                                                     |
| S3      | L1        | NTC            | NT              | PROD VOL       | MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, SL_1_RBT___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__                                                                                                                                                                                                                                           |
| S3      | L1        | NTC            | NT              | PROD COUNT     | MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, SL_1_RBT___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__                                                                                                                                                                                                                                           |
| S3      | L2        | NTC            | NT              | PROD VOL       | OL_2_LFR___, OL_2_LRR___, SL_2_FRP___, SL_2_LST___, SR_2_LAN___, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                                    |
| S3      | L2        | NTC            | NT              | PROD COUNT     | OL_2_LFR___, OL_2_LRR___, SL_2_FRP___, SL_2_LST___, SR_2_LAN___, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                                    |
| S3      |           |                | NR, AL          | PROD TOT VOL   | DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___ |
| S3      |           |                | NT              | PROD TOT VOL   | MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                  |
| S3      |           |                | ST              | PROD TOT VOL   | MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                       |
| S3      |           |                | NR, AL          | PROD TOT COUNT | DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___ |
| S3      |           |                | NT              | PROD TOT COUNT | MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                  |
| S3      |           |                | ST              | PROD TOT COUNT | MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                       |
| S3      | L0        | NRT            | NR, AL          | LTA VOL        | DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, SL_0_SLT___, SR_0_CAL___, SR_0_SRA___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___                                                                                                                                                                          |
| S3      | L0        | NRT            | ST              | LTA VOL        | SR_0_SRA___                                                                                                                                                                                                                                                                                                                                      |
| S3      | L0        | NRT            | NR, AL          | LTA COUNT      | DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, SL_0_SLT___, SR_0_CAL___, SR_0_SRA___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___                                                                                                                                                                          |
| S3      | L0        | NRT            | ST              | LTA COUNT      | SR_0_SRA___                                                                                                                                                                                                                                                                                                                                      |
| S3      | L1        |                | NR, AL          | DD VOL         | MW_1_CAL___, MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, SL_1_RBT___, SR_1_CAL___, SR_1_SRA___                                                                                                                                                                                                                              |
| S3      | L1        |                | NT              | DD VOL         | MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, SL_1_RBT___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__                                                                                                                                                                                                                                           |
| S3      | L1        |                | ST              | DD VOL         | MW_1_MWR___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__                                                                                                                                                                                                                                                                                  |
| S3      | L1        |                | NR, AL          | DD COUNT       | MW_1_CAL___, MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, SL_1_RBT___, SR_1_CAL___, SR_1_SRA___                                                                                                                                                                                                                              |
| S3      | L1        |                | NT              | DD COUNT       | MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, SL_1_RBT___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__                                                                                                                                                                                                                                           |
| S3      | L1        |                | ST              | DD COUNT       | MW_1_MWR___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__                                                                                                                                                                                                                                                                                  |
| S3      | L2        |                | NR, AL          | DD VOL         | OL_2_LFR___, OL_2_LRR___, SL_2_LST___, SR_2_LAN___                                                                                                                                                                                                                                                                                               |
| S3      | L2        |                | NT              | DD VOL         | OL_2_LFR___, OL_2_LRR___, SL_2_FRP___, SL_2_LST___, SR_2_LAN___, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                                    |
| S3      | L2        |                | ST              | DD VOL         | SR_2_LAN___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                                                                                                     |
| S3      | L2        |                | NR, AL          | DD COUNT       | OL_2_LFR___, OL_2_LRR___, SL_2_LST___, SR_2_LAN___                                                                                                                                                                                                                                                                                               |
| S3      | L2        |                | NT              | DD COUNT       | OL_2_LFR___, OL_2_LRR___, SL_2_FRP___, SL_2_LST___, SR_2_LAN___, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                                    |
| S3      | L2        |                | ST              | DD COUNT       | SR_2_LAN___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                                                                                                     |
| S3      |           |                | NR, AL          | DD TOT VOL     | DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___ |
| S3      |           |                | NT              | DD TOT VOL     | MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                  |
| S3      |           |                | ST              | DD TOT VOL     | MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                       |
| S3      |           |                | NR, AL          | DD TOT COUNT   | DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___ |
| S3      |           |                | NT              | DD TOT COUNT   | MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                  |
| S3      |           |                | ST              | DD TOT COUNT   | MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                       |
| S3      | L1        |                | NR, AL          | DL VOL         | MW_1_CAL___, MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, SL_1_RBT___, SR_1_CAL___, SR_1_SRA___                                                                                                                                                                                                                              |
| S3      | L1        |                | NT              | DL VOL         | MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, SL_1_RBT___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__                                                                                                                                                                                                                                           |
| S3      | L1        |                | ST              | DL VOL         | MW_1_MWR___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__                                                                                                                                                                                                                                                                                  |
| S3      | L1        |                | NR, AL          | DL COUNT       | MW_1_CAL___, MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, SL_1_RBT___, SR_1_CAL___, SR_1_SRA___                                                                                                                                                                                                                              |
| S3      | L1        |                | NT              | DL COUNT       | MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, SL_1_RBT___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__                                                                                                                                                                                                                                           |
| S3      | L1        |                | ST              | DL COUNT       | MW_1_MWR___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__                                                                                                                                                                                                                                                                                  |
| S3      | L2        |                | NR, AL          | DL VOL         | OL_2_LFR___, OL_2_LRR___, SL_2_LST___, SR_2_LAN___                                                                                                                                                                                                                                                                                               |
| S3      | L2        |                | NT              | DL VOL         | OL_2_LFR___, OL_2_LRR___, SL_2_FRP___, SL_2_LST___, SR_2_LAN___, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                                    |
| S3      | L2        |                | ST              | DL VOL         | SR_2_LAN___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                                                                                                     |
| S3      | L2        |                | NR, AL          | DL COUNT       | OL_2_LFR___, OL_2_LRR___, SL_2_LST___, SR_2_LAN___                                                                                                                                                                                                                                                                                               |
| S3      | L2        |                | NT              | DL COUNT       | OL_2_LFR___, OL_2_LRR___, SL_2_FRP___, SL_2_LST___, SR_2_LAN___, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                                    |
| S3      | L2        |                | ST              | DL COUNT       | SR_2_LAN___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                                                                                                     |
| S3      |           |                | NR, AL          | DL TOT VOL     | DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___ |
| S3      |           |                | NT              | DL TOT VOL     | MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                  |
| S3      |           |                | ST              | DL TOT VOL     | MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                       |
| S3      |           |                | NR, AL          | DL TOT COUNT   | DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, MW_1_CAL___, MW_1_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_LST___, SR_0_CAL___, SR_0_SRA___, SR_1_CAL___, SR_1_SRA___, SR_2_LAN___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___ |
| S3      |           |                | NT              | DL TOT COUNT   | MW_1_MWR___, OL_0_EFR___, OL_1_EFR___, OL_1_ERR___, OL_2_LFR___, OL_2_LRR___, SL_0_SLT___, SL_1_RBT___, SL_2_FRP___, SL_2_LST___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                  |
| S3      |           |                | ST              | DL TOT COUNT   | MW_1_MWR___, SR_0_SRA___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SR_2_LAN___, SY_1_MISR__, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___                                                                                                                                                                                       |

 Time reference for this dashboard is: sensing_start_date

Important notice: Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## System Technical Budget Schematic View - S5[🔗](https://omcs.copernicus.eu/grafana/d/C-S9wvFVk/system-technical-budget-schematic-view-s5)

**Section**: STB

**Description**: 

The System Technical Budget Schematic View - S5 is based on 



- the data budget reference document [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2).



- the data flow reference document [\[ESA-EOPG-EOPGC-TN-58\] CSC GS Data Flow Configuration.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-58%5D%20CSC%20GS%20Data%20Flow%20Configuration.pdf?api=v2).



Data flow document extraction is visible in the ["Data Flow dashboard"](./d/MfmL_E4Vz/golden-rules-and-data-flow?orgId=1) 



### Data selected



From [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2) document some assuption are made to provide the System Technical Budget dashboards.
a


For System Technical Budget Schematic View - S5 the data published at PRIP, LTA or DD and DSIB files are selected.



 - Section Data Aquisition data from DSIB files.

 - Section Data Production data published at PRIP.

 - Section Data Preservation data published at LTA.

 - Section Data Distribution data published at DD.




**Data collection** are considered as consistent since **01/08/2022**

**Data collection** for **aquisition** are considered as consistent since **15/03/2023**



Values are mean by satellite number in mission. (i.e. S1 1 satellite, S2 mean of 2 satellite, S3 mean of 2 satellite; S5 1 satellite )



For S1, S2, S3 values are mean of the 4 LTA, for S5 values came from S5P_DLR.



Rmq : There is today no S5 L0 data published at prip.



### Annexes



#### Product type selected



The tables below present how products types are classified in STB level and STB timeliness:



##### For panel **Yearly Overall Data Flow S5 SATELLITE**:



|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S5|||NRTI|ACQ VOL|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|||OFFL|ACQ VOL|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|ACQ VOL|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S5|||NRTI|ACQ COUNT|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|||OFFL|ACQ COUNT|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|ACQ COUNT|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S5|L0|NRT-NTC|OPER|PROD VOL|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S5|L0|NRT-NTC|OPER|PROD COUNT|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S5|L1|NRT|NRTI|PROD VOL|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8|
|S5|L1|NRT|NRTI|PROD COUNT|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8|
|S5|L1|NTC|OFFL|PROD VOL|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8|
|S5|L1|NTC|OFFL|PROD COUNT|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8|
|S5|L2|NRT|NRTI|PROD VOL|NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|L2|NRT|NRTI|PROD COUNT|NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|L2|NTC|OFFL|PROD VOL|OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|L2|NTC|OFFL|PROD COUNT|OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|L0||OPER|LTA VOL|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S5|L0||OPER|LTA COUNT|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S5|L1||NRTI|LTA VOL|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8|
|S5|L1||OFFL|LTA VOL|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8|
|S5|L1||NRTI|LTA COUNT|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8|
|S5|L1||OFFL|LTA COUNT|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8|
|S5|L2||NRTI|LTA VOL|NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|L2||OFFL|LTA VOL|OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|L2||NRTI|LTA COUNT|NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|L2||OFFL|LTA COUNT|OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||NRTI|LTA TOT VOL|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|||OFFL|LTA TOT VOL|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|LTA TOT VOL|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S5|||NRTI|LTA TOT COUNT|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|||OFFL|LTA TOT COUNT|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|LTA TOT COUNT|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S5|L1||NRTI|DD VOL|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8|
|S5|L1||OFFL|DD VOL|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8|
|S5|L1||NRTI|DD COUNT|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8|
|S5|L1||OFFL|DD COUNT|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8|
|S5|L2||NRTI|DD VOL|NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|L2||OFFL|DD VOL|OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|L2||NRTI|DD COUNT|NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|L2||OFFL|DD COUNT|OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||NRTI|DD TOT VOL|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|||OFFL|DD TOT VOL|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|DD TOT VOL|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S5|||NRTI|DD TOT COUNT|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|||OFFL|DD TOT COUNT|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|DD TOT COUNT|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S5|L1||NRTI|DL VOL|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8|
|S5|L1||OFFL|DL VOL|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8|
|S5|L1||NRTI|DL COUNT|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8|
|S5|L1||OFFL|DL COUNT|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8|
|S5|L2||NRTI|DL VOL|NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|L2||OFFL|DL VOL|OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|L2||NRTI|DL COUNT|NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|L2||OFFL|DL COUNT|OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||NRTI|Dl TOT VOL|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|||OFFL|Dl TOT VOL|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|Dl TOT VOL|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S5|||NRTI|Dl TOT COUNT|NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8, NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|
|S5|||OFFL|Dl TOT COUNT|OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8, OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|||OPER|Dl TOT COUNT|OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|


Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## System Technical Budget Table - Acquisition[🔗](https://omcs.copernicus.eu/grafana/d/9jt42U2Vz/system-technical-budget-table-acquisition)

**Section**: STB

**Description**: 

The System Technical Budget Tables - Aquisition is based on 

- the data budget reference document [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2).
- the data flow reference document [\[ESA-EOPG-EOPGC-TN-58\] CSC GS Data Flow Configuration.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-58%5D%20CSC%20GS%20Data%20Flow%20Configuration.pdf?api=v2).

Data flow document extraction is visible in the ["Data Flow dashboard"](./d/MfmL_E4Vz/golden-rules-and-data-flow?orgId=1) 

### Data selected

From [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2) document some assuption are made to provide the System Technical Budget dashboards.

For System Technical Budget Tables - Aquisition the data From DSIB are selected.

 - Section Data Aquisition data from DSIB files.


**Data collection** are considered as consistent since **01/08/2022**

**Data collection** for **aquisition** are considered as consistent since **15/03/2023**

Values are mean by downlink (2 channels) by satellite number in mission. (i.e. S1 1 satellite, S2 mean of 2 satellite, S3 mean of 2 satellite; S5 1 satellite )

### Annexes

#### Product type selected

There is no Product type, level or timleiness concept for information about passes transfers.

### Dashboard usage

On left top of the dashboard the mean combobox allow to select mean period:

- none: values for the selected period.
- by day: values are divided by the number of seconds in the selected periode divided by the number of seconds in 1 day.
- by week: values are divided by the number of seconds in the selected periode divided by the number of seconds in 7 day.
- by month: values are divided by the number of seconds in the selected periode divided by the number of seconds in 30 day.
- by year: values are divided by the number of seconds in the selected periode divided by the number of seconds in 365 day.


Time reference for this dashboard is : time_created

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## System Technical Budget Tables - Archiving[🔗](https://omcs.copernicus.eu/grafana/d/nRlrQvKVk/system-technical-budget-tables-archiving)

**Section**: STB

**Description**: 

The System Technical Budget Tables - Archiving is based on 
- the data budget reference document [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2).
- the data flow reference document [\[ESA-EOPG-EOPGC-TN-58\] CSC GS Data Flow Configuration.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-58%5D%20CSC%20GS%20Data%20Flow%20Configuration.pdf?api=v2).

Data flow document extraction is visible in the ["Data Flow dashboard"](./d/MfmL_E4Vz/golden-rules-and-data-flow?orgId=1) 

### Data selected

From [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2) document some assuption are made to provide the System Technical Budget dashboards.
For System Technical Budget Tables - Archiving the data published at LTA are selected.
 - Section Data Preservation data published at LTA.

**Data collection** are considered as consistent since **01/08/2022**

**Data collection** for **aquisition** are considered as consistent since **15/03/2023**

Values are mean by satellite number in mission. (  i.e.  S1  1  satellite,  S2  mean  of  2  satellite,  S3  mean  of  2  satellite;  S5  1  satellite ) 

For S1, S2, S3 values are mean of the 4 LTA, for S5 values came from S5P_DLR.

### Annexes

#### Product type selected

The tables below present how products types are classified in STB level and STB timeliness: 

##### For panel **System Technical Budget (  On  Range ) **: 

|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|L0|NTC|NTC||EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S, RF_RAW, S1_RAW__0A, S1_RAW__0C, S1_RAW__0N, S1_RAW__0S, S2_RAW__0A, S2_RAW__0C, S2_RAW__0N, S2_RAW__0S, S3_RAW__0A, S3_RAW__0C, S3_RAW__0N, S3_RAW__0S, S4_RAW__0A, S4_RAW__0C, S4_RAW__0N, S4_RAW__0S, S5_RAW__0A, S5_RAW__0C, S5_RAW__0N, S5_RAW__0S, S6_RAW__0A, S6_RAW__0C, S6_RAW__0N, S6_RAW__0S, WV_RAW__0A, WV_RAW__0C, WV_RAW__0N, WV_RAW__0S|
|S1|L0|NRT|NRT, NRT-PT||EW_RAW__0A, EW_RAW__0C, EW_RAW__0N, EW_RAW__0S, IW_RAW__0A, IW_RAW__0C, IW_RAW__0N, IW_RAW__0S|
|S1|L1|NTC|NTC||EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S, S1_GRDH_1A, S1_GRDH_1S, S1_SLC__1A, S1_SLC__1S, S2_GRDH_1A, S2_GRDH_1S, S2_SLC__1A, S2_SLC__1S, S3_GRDH_1A, S3_GRDH_1S, S3_SLC__1A, S3_SLC__1S, S4_GRDH_1A, S4_GRDH_1S, S4_SLC__1A, S4_SLC__1S, S5_GRDH_1A, S5_GRDH_1S, S5_SLC__1A, S5_SLC__1S, S6_GRDH_1A, S6_GRDH_1S, S6_SLC__1A, S6_SLC__1S, WV_SLC__1A, WV_SLC__1S|
|S1|L1|NRT|NRT, NRT-PT||EW_GRDM_1A, EW_GRDM_1S, EW_SLC__1A, EW_SLC__1S, IW_GRDH_1A, IW_GRDH_1S, IW_SLC__1A, IW_SLC__1S|
|S1|L2|NTC|NTC||EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S, S1_OCN__2A, S1_OCN__2S, S2_OCN__2A, S2_OCN__2S, S3_OCN__2A, S3_OCN__2S, S4_OCN__2A, S4_OCN__2S, S5_OCN__2A, S5_OCN__2S, S6_OCN__2A, S6_OCN__2S, WV_OCN__2A, WV_OCN__2S|
|S1|L2|NRT|NRT, NRT-PT||EW_OCN__2A, EW_OCN__2S, IW_OCN__2A, IW_OCN__2S|
|S2|L0|NTC|NOMINAL||MSI_L0__DS, MSI_L0__GR|
|S2|L1|NTC|NOMINAL||MSI_L1A_DS, MSI_L1A_GR, MSI_L1B_DS, MSI_L1B_GR, MSI_L1C___, MSI_L1C_DS, MSI_L1C_TC, MSI_L1C_TL|
|S2|L2|NTC|NOMINAL||MSI_L2A___, MSI_L2A_DS, MSI_L2A_TC, MSI_L2A_TL|
|S3|L0|NTC|NT||OL_0_EFR___, SL_0_SLT___|
|S3|L0|NRT|NR, AL||DO_0_DOP___, DO_0_NAV___, GN_0_GNS___, MW_0_MWR___, OL_0_CR0___, OL_0_CR1___, OL_0_EFR___, SL_0_SLT___, SR_0_CAL___, SR_0_SRA___, TM_0_HKM___, TM_0_HKM2__, TM_0_NAT___|
|S3|L0|NRT|ST||SR_0_SRA___|
|S3|L1|NTC|NT||MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, SL_1_RBT___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__|
|S3|L1|NRT|NR, AL||MW_1_CAL___, MW_1_MWR___, OL_1_EFR___, OL_1_ERR___, OL_1_RAC___, OL_1_SPC___, SL_1_RBT___, SR_1_CAL___, SR_1_SRA___|
|S3|L1|NRT|ST||MW_1_MWR___, SR_1_SRA___, SR_1_SRA_A_, SR_1_SRA_BS, SY_1_MISR__|
|S3|L2|NTC|NT||OL_2_LFR___, OL_2_LRR___, SL_2_FRP___, SL_2_LST___, SR_2_LAN___, SY_2_AOD___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S3|L2|NRT|NR, AL||OL_2_LFR___, OL_2_LRR___, SL_2_LST___, SR_2_LAN___|
|S3|L2|NRT|ST||SR_2_LAN___, SY_2_SYN___, SY_2_V10___, SY_2_VG1___, SY_2_VGK___, SY_2_VGP___|
|S5|L0|NTC|OPER||OPER_L0__ENG_A_, OPER_L0__ODB_1_, OPER_L0__ODB_2_, OPER_L0__ODB_3_, OPER_L0__ODB_4_, OPER_L0__ODB_5_, OPER_L0__ODB_6_, OPER_L0__ODB_7_, OPER_L0__ODB_8_, OPER_L0__SAT_A_|
|S5|L1|NTC|OFFL||OFFL_L1B_CA_SIR, OFFL_L1B_CA_UVN, OFFL_L1B_ENG_DB, OFFL_L1B_IR_SIR, OFFL_L1B_IR_UVN, OFFL_L1B_RA_BD1, OFFL_L1B_RA_BD2, OFFL_L1B_RA_BD3, OFFL_L1B_RA_BD4, OFFL_L1B_RA_BD5, OFFL_L1B_RA_BD6, OFFL_L1B_RA_BD7, OFFL_L1B_RA_BD8|
|S5|L1|NRT|NRTI||NRTI_L1B_ENG_DB, NRTI_L1B_RA_BD1, NRTI_L1B_RA_BD2, NRTI_L1B_RA_BD3, NRTI_L1B_RA_BD4, NRTI_L1B_RA_BD5, NRTI_L1B_RA_BD6, NRTI_L1B_RA_BD7, NRTI_L1B_RA_BD8|
|S5|L2|NTC|OFFL||OFFL_L2__03_TCL, OFFL_L2__AER_AI, OFFL_L2__AER_LH, OFFL_L2__CH4_, OFFL_L2__CLOUD_, OFFL_L2__CO____, OFFL_L2__FRESCO, OFFL_L2__HCHO_, OFFL_L2__NO2___, OFFL_L2__NP_BD3, OFFL_L2__NP_BD6, OFFL_L2__NP_BD7, OFFL_L2__O3____, OFFL_L2__O3__PR, OFFL_L2__SO2___|
|S5|L2|NRT|NRTI||NRTI_L2__03_TCL, NRTI_L2__AER_AI, NRTI_L2__AER_LH, NRTI_L2__CLOUD_, NRTI_L2__CO____, NRTI_L2__FRESCO, NRTI_L2__HCCO_, NRTI_L2__NO2___, NRTI_L2__O3____, NRTI_L2__O3__PR, NRTI_L2__SO2___|

##### For the others panel in the dashboard: 

Data cames form System Technical Budget (  On  Range ) panel.

### Dashboard usage

On left top of the dashboard the mean combobox allow to select mean period: 
- by day: values are divided by the number of seconds in the selected periode divided by the number of seconds in 1 day.
- by week: values are divided by the number of seconds in the selected periode divided by the number of seconds in 7 day.
- by month: values are divided by the number of seconds in the selected periode divided by the number of seconds in 30 day.
- by year: values are divided by the number of seconds in the selected periode divided by the number of seconds in 365 day.

Time reference for this dasboard is: sensing_start_date

Important notice: Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## System Technical Budget Tables - Dissemination[🔗](https://omcs.copernicus.eu/grafana/d/2sDjwvFVz/system-technical-budget-tables-dissemination)

**Section**: STB

**Description**: 

<p style="color:#6e9fff;font-size:12px;">⚠️ Data used : DHUS before 30/09/2023 (DHUS decomition), DAS after.</p>


## System Technical Budget Tables - Production[🔗](https://omcs.copernicus.eu/grafana/d/ZJm3wDKVz/system-technical-budget-tables-production)

**Section**: STB

**Description**: 

The System Technical Budget Tables - Production is based on
- the data budget reference document [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2).
- the data flow reference document [\[ESA-EOPG-EOPGC-TN-58\] CSC GS Data Flow Configuration.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-58%5D%20CSC%20GS%20Data%20Flow%20Configuration.pdf?api=v2).

Data flow document extraction is visible in the ["Data Flow dashboard"](./d/MfmL_E4Vz/golden-rules-and-data-flow?orgId=1) 

### Data selected

From [\[ESA-EOPG-EOPGC-TN-9\] CSC Operations – ESA Framework – System Technical Budget.pdf](https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-9%5D%20CSC%20Operations%20%E2%80%93%20ESA%20Framework%20%E2%80%93%20System%20Technical%20Budget.pdf?api=v2) document some assuption are made to provide the System Technical Budget dashboards.


For System Technical Budget Tables - Production the data published at PRIP are selected.

-Section Data Preservation data published at PRIP.

**Data collection** are considered as consistent since **01/08/2022**

**Data collection** for **aquisition** are considered as consistent since **15/03/2023**

Values are mean by satellite number in mission. (i.e. S1 1 satellite, S2 mean of 2 satellite, S3 mean of 2 satellite; S5 1 satellite )

Rmq : There is today no S5 L0 data published at prip.

### Annexes

#### Product type selected

The table below present how products types are classified in STB level and STB timeliness: 

##### For panel**System Technical Budget( On Range)**: 

|Mission|STB Level|STB Timeliness|Real timeliness|Misc.|Product Type|
|---|---|---|---|---|---|
|S1|L0|NTC|NTC||EW_RAW__0A,EW_RAW__0C,EW_RAW__0N,EW_RAW__0S,IW_RAW__0A,IW_RAW__0C,IW_RAW__0N,IW_RAW__0S,RF_RAW,S1_RAW__0A,S1_RAW__0C,S1_RAW__0N,S1_RAW__0S,S2_RAW__0A,S2_RAW__0C,S2_RAW__0N,S2_RAW__0S,S3_RAW__0A,S3_RAW__0C,S3_RAW__0N,S3_RAW__0S,S4_RAW__0A,S4_RAW__0C,S4_RAW__0N,S4_RAW__0S,S5_RAW__0A,S5_RAW__0C,S5_RAW__0N,S5_RAW__0S,S6_RAW__0A,S6_RAW__0C,S6_RAW__0N,S6_RAW__0S,WV_RAW__0A,WV_RAW__0C,WV_RAW__0N,WV_RAW__0S|
|S1|L0|NRT|NRT,NRT-PT||EW_RAW__0A,EW_RAW__0C,EW_RAW__0N,EW_RAW__0S,IW_RAW__0A,IW_RAW__0C,IW_RAW__0N,IW_RAW__0S|
|S1|L1|NRT|NRT,NRT-PT||EW_GRDM_1A,EW_GRDM_1S,EW_SLC__1A,EW_SLC__1S,IW_GRDH_1A,IW_GRDH_1S,IW_SLC__1A,IW_SLC__1S|
|S1|L1|NTC|NTC||EW_GRDM_1A,EW_GRDM_1S,EW_SLC__1A,EW_SLC__1S,IW_GRDH_1A,IW_GRDH_1S,IW_SLC__1A,IW_SLC__1S,S1_GRDH_1A,S1_GRDH_1S,S1_SLC__1A,S1_SLC__1S,S2_GRDH_1A,S2_GRDH_1S,S2_SLC__1A,S2_SLC__1S,S3_GRDH_1A,S3_GRDH_1S,S3_SLC__1A,S3_SLC__1S,S4_GRDH_1A,S4_GRDH_1S,S4_SLC__1A,S4_SLC__1S,S5_GRDH_1A,S5_GRDH_1S,S5_SLC__1A,S5_SLC__1S,S6_GRDH_1A,S6_GRDH_1S,S6_SLC__1A,S6_SLC__1S,WV_SLC__1A,WV_SLC__1S|
|S1|L2|NTC|NTC||EW_OCN__2A,EW_OCN__2S,IW_OCN__2A,IW_OCN__2S,S1_OCN__2A,S1_OCN__2S,S2_OCN__2A,S2_OCN__2S,S3_OCN__2A,S3_OCN__2S,S4_OCN__2A,S4_OCN__2S,S5_OCN__2A,S5_OCN__2S,S6_OCN__2A,S6_OCN__2S,WV_OCN__2A,WV_OCN__2S|
|S1|L2|NRT|NRT,NRT-PT||EW_OCN__2A,EW_OCN__2S,IW_OCN__2A,IW_OCN__2S|
|S2|L0|NTC|NOMINAL||MSI_L0__DS,MSI_L0__GR|
|S2|L1A|NTC|NOMINAL||MSI_L1A_DS,MSI_L1A_GR|
|S2|L1B|NTC|NOMINAL||MSI_L1B_DS,MSI_L1B_GR|
|S2|L1C|NTC|NOMINAL||MSI_L1C___,MSI_L1C_DS,MSI_L1C_TC,MSI_L1C_TL|
|S2|L2A|NTC|NOMINAL||MSI_L2A___,MSI_L2A_DS,MSI_L2A_TC,MSI_L2A_TL|
|S3|L0|NTC|NT||OL_0_EFR___,SL_0_SLT___|
|S3|L0|NRT|NR,AL||DO_0_DOP___,DO_0_NAV___,GN_0_GNS___,MW_0_MWR___,OL_0_CR0___,OL_0_CR1___,OL_0_EFR___,SL_0_SLT___,SR_0_CAL___,SR_0_SRA___,TM_0_HKM___,TM_0_HKM2__,TM_0_NAT___|
|S3|L0|NRT|ST||SR_0_SRA___|
|S3|L1|NTC|NT||MW_1_MWR___,OL_1_EFR___,OL_1_ERR___,SL_1_RBT___,SR_1_SRA___,SR_1_SRA_A_,SR_1_SRA_BS,SY_1_MISR__|
|S3|L1|NRT|NR,AL||MW_1_CAL___,MW_1_MWR___,OL_1_EFR___,OL_1_ERR___,OL_1_RAC___,OL_1_SPC___,SL_1_RBT___,SR_1_CAL___,SR_1_SRA___|
|S3|L1|NRT|ST||MW_1_MWR___,SR_1_SRA___,SR_1_SRA_A_,SR_1_SRA_BS,SY_1_MISR__|
|S3|L2|NTC|NT||OL_2_LFR___,OL_2_LRR___,SL_2_FRP___,SL_2_LST___,SR_2_LAN___,SY_2_AOD___,SY_2_SYN___,SY_2_V10___,SY_2_VG1___,SY_2_VGK___,SY_2_VGP___|
|S3|L2|NRT|NR,AL||OL_2_LFR___,OL_2_LRR___,SL_2_LST___,SR_2_LAN___|
|S3|L2|NRT|ST||SR_2_LAN___,SY_2_SYN___,SY_2_V10___,SY_2_VG1___,SY_2_VGK___,SY_2_VGP___|
|S5|L0|NTC|OPER||OPER_L0__ENG_A_,OPER_L0__ODB_1_,OPER_L0__ODB_2_,OPER_L0__ODB_3_,OPER_L0__ODB_4_,OPER_L0__ODB_5_,OPER_L0__ODB_6_,OPER_L0__ODB_7_,OPER_L0__ODB_8_,OPER_L0__SAT_A_|
|S5|L1|NTC|OFFL||OFFL_L1B_CA_SIR,OFFL_L1B_CA_UVN,OFFL_L1B_ENG_DB,OFFL_L1B_IR_SIR,OFFL_L1B_IR_UVN,OFFL_L1B_RA_BD1,OFFL_L1B_RA_BD2,OFFL_L1B_RA_BD3,OFFL_L1B_RA_BD4,OFFL_L1B_RA_BD5,OFFL_L1B_RA_BD6,OFFL_L1B_RA_BD7,OFFL_L1B_RA_BD8|
|S5|L1|NRT|NRTI||NRTI_L1B_ENG_DB,NRTI_L1B_RA_BD1,NRTI_L1B_RA_BD2,NRTI_L1B_RA_BD3,NRTI_L1B_RA_BD4,NRTI_L1B_RA_BD5,NRTI_L1B_RA_BD6,NRTI_L1B_RA_BD7,NRTI_L1B_RA_BD8|
|S5|L2|NTC|OFFL||OFFL_L2__03_TCL,OFFL_L2__AER_AI,OFFL_L2__AER_LH,OFFL_L2__CH4_,OFFL_L2__CLOUD_,OFFL_L2__CO____,OFFL_L2__FRESCO,OFFL_L2__HCHO_,OFFL_L2__NO2___,OFFL_L2__NP_BD3,OFFL_L2__NP_BD6,OFFL_L2__NP_BD7,OFFL_L2__O3____,OFFL_L2__O3__PR,OFFL_L2__SO2___|
|S5|L2|NRT|NRTI||NRTI_L2__03_TCL,NRTI_L2__AER_AI,NRTI_L2__AER_LH,NRTI_L2__CLOUD_,NRTI_L2__CO____,NRTI_L2__FRESCO,NRTI_L2__HCCO_,NRTI_L2__NO2___,NRTI_L2__O3____,NRTI_L2__O3__PR,NRTI_L2__SO2___|

#####Fortheotherspanelinthedashboard: 

Data cames form System Technical Budget( On Range) panel.

### Dashboard usage

On left top of the dashboard the mean combobox allow to select mean period: 
- by day: values are divided by the number of seconds in the selected periode divided by the number of seconds in 1 day.
- by week: values are divided by the number of seconds in the selected periode divided by the number of seconds in 7 day.
- by month: values are divided by the number of seconds in the selected periode divided by the number of seconds in 30 day.
- by year: values are divided by the number of seconds in the selected periode divided by the number of seconds in 365 day.

Time reference for this dashboard is: sensing_start_date

Important notice: Tables & timelines can only display up to 10000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## System Technical Budget Thresholds[🔗](https://omcs.copernicus.eu/grafana/d/aditsrffkv94wd/system-technical-budget-thresholds)

**Section**: STB

**Description**: 

#### Summary ##
This dashboard features a comparison between the real amount of element and volumes in the database in regards with the budgeted values given in the technical budget thanks to red thresholds displayed on graphs.

The dashboard is split in 2 rows:
- The first row gives a global overview per service type : ```Production, Archiving and Dissemination``` per satellite. In green, the volume/count in our database and in red the budgeted value. The satelite and mission can be chosen

- The second row gives a more detailled view where user can also choose a specific technocal budget level and timeliness for a giner granularity
 

#### Timeliness lookup table ##

To match the timeliness written in the technical budget with the one from our database, the following true table has been used

    Technical budget MISSION // Technical budget Timeliness // Database timelinesses

    S1    ///    NTC      ///   ["NTC"]
    S1    ///    NRT:     ///   ["NRT","NRT-PT"]
    S1    ///    A        ///   ["NRT-PT","NTC","NRT"]
    S1    ///    AUX      ///   ["_"]
    S1    ///    _        ///   ["_"]


    S2    ///    NTC      ///   ["NOMINAL,NOT_RECORDING"]
    S2    ///    AUX      ///   ["AUX"]
    S2    ///    _        ///   ["_"]


    S3    ///    NTC      ///   ["NT"]
    S3    ///    NRT      ///   ["NR,AL"]
    S3    ///    STC      ///   ["ST"]
    S3    ///    AUX      ///   ["SN,NS,NN,_"]


    S5    ///    NTC      ///   ["OPER,OFFL"]
    S5    ///    AUX      ///   ["_"]
    S5    ///    NRT      ///   ["NRTI"]


#### Facts related to technical budget v1.8 ##

- element in technical budget with level L1X are rattached to L1.  EG: L1B -> L1  etc..

- the typo in technical budget  type ```OFFL_L2__HCCO_``` instead of ```OFFL_L2__HCHO_``` has been taken into account in our calculation

- type ```OBS_SS__` ``` is not an AUX and has not level so it has been disregarded from our calculation

- All auxiliary have their level defined to ```AUX``` even if not written in the databudget

- Some types in the technical budget have a suffix which does not exist for elements in our database ```(AUX_ECE)   (EUP)   (SH/SV/DH/DV)  (SH/SV) ``` so they have been removed to match with our data

- Somes element in the databudget have their field ```#Num/day``` and/or ```Volume per day [GB]``` not defined. It will lead to an incomplete threshold definition

- Some element for mission S1 have their level set to A without a timeliness defined. We kept them in a separate A level and we associated it to timeliness ["NRT-PT","NTC","NRT"] as a guess

#### Note ## 
- It is possible to select the version of the technical budget to use by modifying the version variable
- The granularity of the data is a day


 Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.",


## LTA Alignement[🔗](https://omcs.copernicus.eu/grafana/d/fcd80751-254b-4933-9f3d-588eb26028a9/lta-alignement)

**Section**: Specific

**Description**: 

This dashboard features a comparison of archived product on all LTA

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Acquisition Timeliness[🔗](https://omcs.copernicus.eu/grafana/d/ArGraZm4kgdfg/acquisition-timeliness)

**Section**: Timeliness

**Description**: 

This dashboard features an Acquisition Timeliness for Mission S1, S2, S3, S5.

Information is taken from station reports made available through CADIP interface for S1,S2,S3 and XBAND for S5


Timeliness is computed using following logics : 
- (stop_delivery date - first_frame_start date) for mission S1,S2 and S3
- (delivery_stop date - downlink_start date) for mission S5

Discrepancies are displayed through the following indicators:

- Percent of products below timeliness threshold;
- Average timeliness of products;
- Time series of product displayed against the timeliness threshold;
- Detailed list of product out of accepted range.

Tips:
 - Annotations are available on time series;
 - Satellite, mission, reception station or downlink orbit to consider can be selected in the upper bar.
- Use Downlink Orbit Cadip to filter the downlink orbit for mission S1,S2 and S3
- Use Downlink Orbit DDP to filter the downlink orbit for mission S5

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.



## ADG Timeliness[🔗](https://omcs.copernicus.eu/grafana/d/LYiLzXw8k/adg-timeliness)

**Section**: Timeliness

**Description**: 

This dashboard features a Timeliness computation of data published at the following interfaces:
 - AUXIP.

Auxiliary data is divided into two categories:
 - Several per day (timeliness should be below 10 minutes);
 - One per day (timeliness should be below 30 minutes).

The list of products and their associated frequency :

| Timeliness                | Product Type                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Several per day (<10 min) | AUX_WND, AUX_PREORB, AUX_RESORB, AUX_POEORB, AUX_ECMWFD, AX___MF1_AX, AX___MFA_AX, AX___MA1_AX, AX___MF2_AX, AX___MA2_AX, SR___MDO_AX, SR_2_RMO_AX, SR_2_PMO_AX                                                                                                                                                                                                                                                                                           |
| One per day (<30 min)     | AUX_ICE, AUX_TRO, MPL_ORBPRE, MPL_ORBRES, MPL_TLEPRE, TLM__REQ_B, TLM__REQ_C, TLM__REQ_D, TLM__REQ_E, TLM__REQ_F, AUX_CAMSFO, AUX_UT1UTC, TLM__REQ_A, TLM__REQ_B, REP__CHF__, REP__FCHF__, MPL_ORBPRE, MPL_ORBRES, SR_2_PMPSAX, SR_2_POL_AX, SR_2_PGI_AX, SR_2_RGI_AX, SR_1_USO_AX, SR___MGNSAX, SL_2_SSTAAX, SL_2_DIMSAX, AX___FPO_AX, AX___FRO_AX, AUX_POEORB, AUX_GNSSRD, SR_2_PCPPAX, SR_2_PMPPAX, SR___MGNPAX, SR___POEPAX, SR_2_SIFNAX, SR_2_SIFSAX |

Timeliness is computed from metadata attached to each Auxiliary data (Publication Date - Origin Date).

Discrepancies are displayed through the following indicators:
 - Percent of data below timeliness threshold;
 - Average timeliness of data;
 - Time series of data displayed against the timeliness threshold;
 - Detailed list of data out of accepted range.

Information is available for each mission managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Mission to consider can be selected in the upper bar.


Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## DD Timeliness[🔗](https://omcs.copernicus.eu/grafana/d/ede54e59-bc3d-4e34-bcaf-8b95adf31358/dd-timeliness)

**Section**: Timeliness

**Description**: 

### DDs Timeliness
This dashboard show statistics about the DD product timeliness.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## LTA Timeliness[🔗](https://omcs.copernicus.eu/grafana/d/f36f5bb3-6465-4a54-a35b-9ce4c0838ea6/lta-timeliness)

**Section**: Timeliness

**Description**: 

### LTAs Timeliness
This dashboard show statistics about the LTA product timeliness.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## PRIP-LTA Timeliness[🔗](https://omcs.copernicus.eu/grafana/d/ZrsG86xnl/prip-lta-timeliness)

**Section**: Timeliness

**Description**: 

### LTAs Timeliness
This dashboard show statistics about the LTA product timeliness.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S1 E2E Timeliness (Disseminated from Sensing)[🔗](https://omcs.copernicus.eu/grafana/d/239nDaQnk/s1-e2e-timeliness-disseminated-from-sensing)

**Section**: Timeliness

**Description**: 

This dashboard features a Timeliness computation of products published at the following interfaces for S1 mission:
 - DD DHUS, DAS.

Timeliness is computed from metadata attached to each DD product (Publication Date - Content Date/End (which is the end of sensing)).

Discrepancies are displayed through the following indicators:
 - Percent of products below timeliness threshold;
 - Average timeliness of products;
 - Time series of product displayed against the timeliness threshold;
 - Detailed list of product out of accepted range.

Information is available for each satellite managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.
 - Dissemination service to consider can be selected in the upper bar filter named "Dissemination service".

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S1 E2E Timeliness (Production from Sensing)[🔗](https://omcs.copernicus.eu/grafana/d/ArGraZm4k/s1-e2e-timeliness-production-from-sensing)

**Section**: Timeliness

**Description**: 

This dashboard features a Timeliness computation of products published at the following interfaces for S1 mission:
 - PRIP.

Timeliness is computed from metadata attached to each PRIP product (Publication Date - Content Date/End (which is the end of sensing)).

Discrepancies are displayed through the following indicators:
 - Percent of products below timeliness threshold;
 - Average timeliness of products;
 - Time series of product displayed against the timeliness threshold;
 - Detailed list of product out of accepted range.

Information is available for each satellite managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S1 E2E Timeliness[🔗](https://omcs.copernicus.eu/grafana/d/acb0846e-e67e-4643-8d0c-e9703209e16f/s1-e2e-timeliness)

**Section**: Timeliness

**Description**: 

This dashboard features a Timeliness computation of products published at the following interfaces for S1 mission:
 - DD DHUS, DAS.

Timeliness is computed from metadata attached to each DD product (Publication Date - Content Date/End (which is the end of sensing)).

Discrepancies are displayed through the following indicators:
 - Percent of products below timeliness threshold;
 - Average timeliness of products;
 - Time series of product displayed against the timeliness threshold;
 - Detailed list of product out of accepted range.

Information is available for each satellite managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.
 - Dissemination service to consider can be selected in the upper bar filter named "Dissemination service".

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S2 E2E Timeliness (Disseminated from Sensing)[🔗](https://omcs.copernicus.eu/grafana/d/LYiLzXw7k/s2-e2e-timeliness-disseminated-from-sensing)

**Section**: Timeliness

**Description**: 

This dashboard features a Timeliness computation of products published at the following interfaces for S2 mission:
 - DD DHUS, DAS.

Timeliness is computed from metadata attached to each DD product (Publication Date - Content Date/End (which is the end of sensing)).

Discrepancies are displayed through the following indicators:
 - Percent of products below timeliness threshold;
 - Average timeliness of products;
 - Time series of product displayed against the timeliness threshold;
 - Detailed list of product out of accepted range.

Information is available for each satellite managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.
 - Dissemination service to consider can be selected in the upper bar filter named "Dissemination service".

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S2 E2E Timeliness (Production from Sensing)[🔗](https://omcs.copernicus.eu/grafana/d/_G89-WmVz/s2-e2e-timeliness-production-from-sensing)

**Section**: Timeliness

**Description**: 

This dashboard features a Timeliness computation of products published at the following interfaces for S2 mission:
 - PRIP.

Timeliness is computed from metadata attached to each PRIP product (Publication Date - Content Date/End (which is the end of sensing)).

Discrepancies are displayed through the following indicators:
 - Percent of products below timeliness threshold;
 - Average timeliness of products;
 - Time series of product displayed against the timeliness threshold;
 - Detailed list of product out of accepted range.

Information is available for each satellite managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S2 E2E Timeliness[🔗](https://omcs.copernicus.eu/grafana/d/d4a5e625-c992-4a4a-a66e-7da779b7a044/s2-e2e-timeliness)

**Section**: Timeliness

**Description**: 

This dashboard features a Timeliness computation of products published at the following interfaces for S2 mission:
 - DD DHUS, DAS.

Timeliness is computed from metadata attached to each DD product (Publication Date - Content Date/End (which is the end of sensing)).

Discrepancies are displayed through the following indicators:
 - Percent of products below timeliness threshold;
 - Average timeliness of products;
 - Time series of product displayed against the timeliness threshold;
 - Detailed list of product out of accepted range.

Information is available for each satellite managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.
 - Dissemination service to consider can be selected in the upper bar filter named "Dissemination service".

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S3 E2E Timeliness (Disseminated from Sensing)[🔗](https://omcs.copernicus.eu/grafana/d/QyIDnuQ7k/s3-e2e-timeliness-disseminated-from-sensing)

**Section**: Timeliness

**Description**: 

This dashboard features a Timeliness computation of products published at the following interfaces for S3 mission:
 - DD DHUS, DAS.

Timeliness is computed from metadata attached to each DD product (Publication Date - Content Date/End (which is the end of sensing)).

Discrepancies are displayed through the following indicators:
 - Percent of products below timeliness threshold;
 - Average timeliness of products;
 - Time series of product displayed against the timeliness threshold;
 - Detailed list of product out of accepted range.

Information is available for each satellite managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.
 - Dissemination service to consider can be selected in the upper bar filter named "Dissemination service".

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S3 E2E Timeliness (Production from Sensing)[🔗](https://omcs.copernicus.eu/grafana/d/d5XUaWiVk/s3-e2e-timeliness-production-from-sensing)

**Section**: Timeliness

**Description**: 

This dashboard features a Timeliness computation of products published at the following interfaces for S3 mission:
 - PRIP.

Timeliness is computed from metadata attached to each PRIP product (Publication Date - Content Date/End (which is the end of sensing)).

Discrepancies are displayed through the following indicators:
 - Percent of products below timeliness threshold;
 - Average timeliness of products;
 - Time series of product displayed against the timeliness threshold;
 - Detailed list of product out of accepted range.

Information is available for each satellite managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S5 E2E Timeliness (Disseminated from Sensing)[🔗](https://omcs.copernicus.eu/grafana/d/LYq4MSC7z/s5-e2e-timeliness-disseminated-from-sensing)

**Section**: Timeliness

**Description**: 

This dashboard features a Timeliness computation of products published at the following interfaces for S5 mission:
 - DD DHUS, DAS.

Timeliness is computed from metadata attached to each DD product (Publication Date - Content Date/End (which is the end of sensing)).

Discrepancies are displayed through the following indicators:
 - Percent of products below timeliness threshold;
 - Average timeliness of products;
 - Time series of product displayed against the timeliness threshold;
 - Detailed list of product out of accepted range.

Information is available for each satellite managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar. 
 - Dissemination service to consider can be selected in the upper bar filter named "Dissemination service".

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## S5 E2E Timeliness (Production from Sensing)[🔗](https://omcs.copernicus.eu/grafana/d/LPt_-Wm4k/s5-e2e-timeliness-production-from-sensing)

**Section**: Timeliness

**Description**: 

This dashboard features a Timeliness computation of products published at the following interfaces for S5 mission:
 - PRIP.

Timeliness is computed from metadata attached to each PRIP product (Publication Date - Content Date/End (which is the end of sensing)).

Discrepancies are displayed through the following indicators:
 - Percent of products below timeliness threshold;
 - Average timeliness of products;
 - Time series of product displayed against the timeliness threshold;
 - Detailed list of product out of accepted range.

Information is available for each satellite managed by OMCS.

Tips:
 - Annotations are available on time series;
 - Satellite to consider can be selected in the upper bar.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Services Timeliness & Production time[🔗](https://omcs.copernicus.eu/grafana/d/CdIGZab7azazaz/services-timeliness-and-production-time)

**Section**: Timeliness

**Description**: 

This dashboard features a Timeliness computation of products published at the following interfaces:
 - PRIP;
 - LTA;
 - DD DHUS.

Timeliness is computed from metadata attached to each product:
 - Production Time is (Publication Date - Origin Date);
 - From sensing timeliness (Publication Date - Content Date/End (which is the end of sensing)).

Discrepancies are displayed through the following indicators:
 - Minimum, maximum, average timeliness;
 - Distribution of timeliness in various time ranges.

Information is available for each mission and interface managed by OMCS.

Tips:
 - Mission to consider can be selected in the upper bar.

Note: Some product category are not disseminated to DHUS

- For S1, S2 and S3, files without timeliness (“_” Category), following product types are concerned :
  - S1 : HTKM and GP files
  - S2 : HKTM and SADATA files
  - S3 : POD, Mission Planning files and Unavailability reports
  
- For S3, products with timeliness AL, NN, NS & SN 

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Satellite Unavailability Reports[🔗](https://omcs.copernicus.eu/grafana/d/FJ9XE528k/satellite-unavailability-reports)

**Section**: Unavailability

**Description**: 

This dashboard features Satellite Unavailability report published at the following interface:
 - AUXIP.

Information is available for the following missions: S1 and S2.

Time reference for this dashboard is : start_time

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Available Data Volume (CADIP)[🔗](https://omcs.copernicus.eu/grafana/d/available-data-volume-cadip/available-data-volume-cadip)

**Section**: Volumes_Count

**Description**: 

This dashboard shows volume of data acquired by stations and made available to Production Services through CADIP interface.


Time reference for this dashboard is : planned_data_start

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Available Data Volume (XBIP / EDRS)[🔗](https://omcs.copernicus.eu/grafana/d/NKq_TCtnz/available-data-volume-xbip-edrs)

**Section**: Volumes_Count

**Description**: 

This dashboard shows volume of data acquired by stations and made available to Production Services through DDP/XBIP interface.


Time reference for this dashboard is : time_created

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Golden rules & Data flow[🔗](https://omcs.copernicus.eu/grafana/d/MfmL_E4Vz/golden-rules-and-data-flow)

**Section**: Volumes_Count

**Description**: 

This view provides the dataflow of Sentinel products as defined in <a href="https://omcs.atlassian.net/wiki/download/attachments/66158618/%5BESA-EOPG-EOPGC-TN-58%5D%20CSC%20GS%20Data%20Flow%20Configuration.pdf?api=v2"> [ESA-EOPG-EOPGC-TN-58] CSC GS Data Flow Configuration</a> document.
<br>
Current dataflow verion is 1.2 .
<br>
Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## LTA Usage[🔗](https://omcs.copernicus.eu/grafana/d/BYUqN6PVz/lta-usage)

**Section**: Volumes_Count

**Description**: 

Time reference for this dashboard is : timestamp

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Products Data Volume and Count[🔗](https://omcs.copernicus.eu/grafana/d/K-JTm_57k/products-data-volume-and-count)

**Section**: Volumes_Count

**Description**: 

This dashboard features statistics on:
 - Product Count (number of individual products published);
 - Data Volume (size of all the products published).

Statistics are available for each interface managed by OMCS.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Products Detailed View (Count Volume and List)[🔗](https://omcs.copernicus.eu/grafana/d/wAz0kHcnk/products-detailed-view-count-volume-and-list)

**Section**: Volumes_Count

**Description**: 

This dashboard features a detailed view of products published on CSC interfaces (PRIP, LTA, ...):
 - Product Count & Volume sorted by product level (L0, L1, L2);
 - Product Count & Volume over time; 
 - Detailled list of products published.


[Golden rules and Data Flow dashboard](./d/MfmL_E4Vz/golden-rules-and-data-flow?orgId=1) provides a view about where to expect each type of product.
In order to finley analyse misalignment between interfaces, please use LTA & DD Completeness dashboards.

Note : The "Range" values provided in legend of Bargraphs, corresponds to the maximum difference observed in product count/volume between displayed services. 

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.


## Products Inventory[🔗](https://omcs.copernicus.eu/grafana/d/zASfw_wnk/products-inventory)

**Section**: Volumes_Count

**Description**: 

This dashboard features information on:
 - Detailed list of published products and date of publication on each interface.

Time reference for this dashboard is : sensing_start_date

Important notice : Tables & timelines can only display up to 10 000 entries. Please make use of filters to narrow down the retrieved data and get a more realistic view.

