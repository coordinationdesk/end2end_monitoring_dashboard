# maas-engine performance guide

## Design tips

### Careful logging

Using `to_dict()` method of documents consumes a lot of time because of serialization: it's ok to use it but **only in ERROR messages**, not in INFO or worse: DEBUG.

### Light queries

- **no wildcard**, _especially on high volume_
- **no scoring**: use _bool filter_, not _match_

### Think bulk

Making a lot of single queries to elastic search leads to poor performance. It's better to group queries to lower the number of network access of HTTP queries.

Before processing a set of documents through, think about the dependencies of the data to load them in a minimal number of queries, creating bulk data loading steps in algorithms.

Try using map / zip in the Python implementation.

### MultiSearch

MultiSearch is a good way to group queries while reading linked data, but it has a limitation: results can not carry versioning metadata, so linked documents can not be written back.

Not necessarily a strong drawback (queries can be ultimately optimized to only retrieve linked documents identifiers instead of whole document bodies), calling `MAASDocument.mget_by_ids()` after is faster than single queries.

## Run scenario

### Database state

Recovering a consistent snapshot may not be always possible, especially during the development of a new feature that does not require the full production backup to be validated.

To create an initial state, a set of file has to be selected in the production backup. This can be a tedious activity, as data dependencies and obscure business logic increase with business complexity.

Ideally, end-to-end testing should match the dataset that validates feature development.

### message payload

TBW

## Using maas_engine_cli

TBW

## Profiling

TBW

## Using IVV resources

Using a remote database is a good way to verify MultiSearch optimizations.

## Get KPI from logs

### logcli

```bash
logcli-linux-amd64 query --timezone=UTC --since=4h '{job="preprod-etl/maas-engine-collect"}' --limit=500000000 --batch=5000 -o raw | grep "created," > engine.log
```

### maas_engine_stats

This tiny cli tool outputs a markdown report for 2 KPI using engine log files:

- execution duration
- rate of processed documents to database

The tables have the following column:

- engine name
- number of calls
- minimum value
- mean value
- maximum value
- standard deviation

#### Interpreting results

- before considering any number as interesting, verify the number of calls

- before thinking a mean is interesting, check the standard deviation
- no day is the same on production when ingesting real data

#### Running

Simply pass a log file as first argument:

```bash
❯ maas_engine_stats preprod_20230421T0849.log
```

#### Duration summary in seconds

These engine statistics are ordered by cumulated execution time.

It can _somehow_ answer the question : what was the cluster doing during all this time ?

Mean values have to be considered with the standard deviation value that is high most of the time.

Thus, cumulated time and maximum duration are good indicators to identify possible optimizations.

|                    Engine                    | Calls |  Min  |  Mean  |  Max   |  Std   |    Cum    |   %   |
| :------------------------------------------: | :---: | :---: | :----: | :----: | :----: | :-------: | :---: |
|          ComputeCompletenessEngine           | 3575  | 0.003 | 10.620 | 97.391 | 13.440 | 37967.060 | 53.66 |
|        PublicationConsolidatorEngine         | 21732 | 0.039 | 0.640  | 33.022 | 0.910  | 13907.116 | 19.66 |
|        ComputeContainerRelatedEngine         | 4065  | 0.058 | 1.646  | 12.702 | 1.012  | 6691.277  | 9.46  |
|         DDProductConsolidatorEngine          | 18385 | 0.019 | 0.240  | 3.425  | 0.169  | 4416.341  | 6.24  |
|         LTAProductConsolidatorEngine         | 1379  | 0.036 | 2.195  | 42.048 | 2.869  | 3027.488  | 4.28  |
|          ProductConsolidatorEngine           | 1968  | 0.038 | 1.190  | 10.572 | 0.720  | 2341.575  | 3.31  |
|        ComputeContainerProductsEngine        | 1669  | 0.013 | 0.694  | 16.235 | 1.272  | 1158.748  | 1.64  |
|         ComputeS3CompletenessEngine          |  193  | 0.012 | 4.268  | 36.958 | 6.341  |  823.695  | 1.16  |
|         ComputeS5CompletenessEngine          |  147  | 0.042 | 2.094  | 24.219 | 4.208  |  307.823  | 0.44  |
|               ReplicatorEngine               |  298  | 0.020 | 0.165  | 0.412  | 0.070  |  49.102   | 0.07  |
|          DeletionConsolidatorEngine          |  262  | 0.028 | 0.173  | 1.131  | 0.174  |  45.260   | 0.06  |
|      DdpDataAvailableConsolidatorEngine      |  139  | 0.017 | 0.051  | 0.527  | 0.063  |   7.135   | 0.01  |
|   ConsolidateAnomalyCorrelationFileEngine    |  10   | 0.132 | 0.402  | 0.842  | 0.226  |   4.016   | 0.01  |
|         ComputeCamsReferencesEngine          |  34   | 0.014 | 0.061  | 0.302  | 0.064  |   2.091   | 0.00  |
| XBandAcquisitionPassStatusConsolidatorEngine |   5   | 0.030 | 0.131  | 0.223  | 0.075  |   0.656   | 0.00  |
| EDRSAcquisitionPassStatusConsolidatorEngine  |   1   | 0.187 | 0.187  | 0.187  | 0.000  |   0.187   | 0.00  |
|  S5AcquisitionPassStatusConsolidatorEngine   |   1   | 0.094 | 0.094  | 0.094  | 0.000  |   0.094   | 0.00  |
|     SatUnavailabilityConsolidatorEngine      |   2   | 0.037 | 0.042  | 0.047  | 0.005  |   0.084   | 0.00  |
|                    Total                     | 53865 |       |        |        |        | 70749.748 |       |

#### Performance summary in document per second

These statistics are ordered by mean value, descendant, and are interesting for consolidation engine and other engine processing a lot of documents to measure document bandwidth.

Call count is important as too small set may lead to too high performances.

|                    Engine                    | Calls |   Min   |  Mean   |   Max    |   Std   |
| :------------------------------------------: | :---: | :-----: | :-----: | :------: | :-----: |
|               ReplicatorEngine               |  298  | 12.195  | 708.268 | 1882.353 | 366.951 |
|          ProductConsolidatorEngine           | 1968  |  0.000  | 423.089 | 844.291  | 168.902 |
|         DDProductConsolidatorEngine          | 18385 |  0.000  | 353.540 | 653.595  | 210.323 |
|        PublicationConsolidatorEngine         | 21732 |  2.288  | 331.200 | 746.356  | 166.724 |
| EDRSAcquisitionPassStatusConsolidatorEngine  |   1   | 267.380 | 267.380 | 267.380  |  0.000  |
|         LTAProductConsolidatorEngine         | 1379  |  4.082  | 265.154 | 912.150  | 215.279 |
| XBandAcquisitionPassStatusConsolidatorEngine |   5   | 17.937  | 160.799 | 557.252  | 200.036 |
|  S5AcquisitionPassStatusConsolidatorEngine   |   1   | 148.936 | 148.936 | 148.936  |  0.000  |
|        ComputeContainerRelatedEngine         | 4065  |  0.000  | 87.475  | 255.072  | 33.819  |
|      DdpDataAvailableConsolidatorEngine      |  139  |  3.247  | 47.963  | 157.895  | 25.960  |
|     SatUnavailabilityConsolidatorEngine      |   2   | 21.277  | 24.152  |  27.027  |  2.875  |
|        ComputeContainerProductsEngine        | 1669  |  0.000  | 10.681  | 112.108  | 18.133  |
|          DeletionConsolidatorEngine          |  262  |  0.000  |  7.372  | 350.685  | 37.992  |
|         ComputeS5CompletenessEngine          |  147  |  0.000  |  7.006  |  32.844  |  8.168  |
|         ComputeS3CompletenessEngine          |  193  |  0.000  |  4.583  |  19.120  |  3.597  |
|   ConsolidateAnomalyCorrelationFileEngine    |  10   |  0.000  |  4.155  |  15.209  |  4.531  |
|          ComputeCompletenessEngine           | 3575  |  0.000  |  0.454  |  17.544  |  1.178  |
|         ComputeCamsReferencesEngine          |  34   |  0.000  |  0.000  |  0.000   |  0.000  |
|                    Total                     | 53865 |         |         |          |         |
