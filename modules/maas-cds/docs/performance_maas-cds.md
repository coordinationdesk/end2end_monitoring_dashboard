# maas-cds and the quest for performances

## 1.13 Tagada: identifying bottleneck and first actions

After another crisis with queues occupied by thousands of slow messages (when DAS data distribution service went to production), a look at what could be done to improve the global performance was necessary.

We already knew that multiplying database queries kills global speed, so looking at all single queries inside for loops was the first target, adding a "TODO FIXME" comment to the source code and then define priorities.

Considering the volume of data, datatake attachment to products and publications appeared like a good start point to try using MultiSearch, because of the large S2 data volume.

### Actions

#### Global scope

- identification of single element queries and prioritize their refactoring
- increase chunk size

#### maas-engine

- add pre / post consolidate template methods to RawDataEngine to pre / post process data in a bulk way
- minimal log analysis script to report 2 KPI per engine: cumulated time and produced document/s

#### maas-cds

- bulk datatake attachment to product and publication engines using MultiSearch and maas-engine pre / post consolidation hooks.

### Effects

No automated deep log analysis at the moment for comparison.

Also, back then, the cluster was sometime saturated with DAS products and their heavy container processing.

#### RabbitMQ

- lower message count in all the queues due to chunk size increased in collector
- more moments where queues are empty

#### opensearch

- load average decreased from 8 to 6
- network increased from 2 to 4 MB/s

### Metrics

_Non-significant entries have been stripped but total kept_.

#### Duration summary in seconds

|            Engine             | Calls |  Min  |  Mean   |   Max   |  Std   |    Cum     |   %   |
| :---------------------------: | :---: | :---: | :-----: | :-----: | :----: | :--------: | :---: |
| ComputeContainerRelatedEngine | 2084  | 0.501 | 101.878 | 544.548 | 91.799 | 212314.471 | 27.41 |
|   ProductConsolidatorEngine   | 5715  | 0.203 | 29.095  | 491.838 | 49.009 | 166279.320 | 21.46 |
|   ComputeCompletenessEngine   | 8135  | 0.005 | 19.469  | 134.530 | 17.588 | 158382.472 | 20.45 |
| PublicationConsolidatorEngine | 13461 | 0.170 |  9.141  | 139.929 | 9.006  | 123045.748 | 15.88 |
| LTAProductConsolidatorEngine  | 5509  | 0.209 | 11.782  | 131.201 | 10.813 | 64909.085  | 8.38  |
|  DDProductConsolidatorEngine  | 2237  | 0.190 |  3.115  | 16.241  | 2.328  |  6968.342  | 0.90  |
|             Total             | 49435 |       |         |         |        | 774653.837 |       |

#### Performance summary in document per second

|            Engine             | Calls |  Min  |  Mean  |   Max   |  Std   |
| :---------------------------: | :---: | :---: | :----: | :-----: | :----: |
| PublicationConsolidatorEngine | 13461 | 0.000 | 49.489 | 204.880 | 34.195 |
| LTAProductConsolidatorEngine  | 5509  | 0.000 | 48.827 | 252.715 | 39.353 |
|   ProductConsolidatorEngine   | 5715  | 0.072 | 43.520 | 287.479 | 41.871 |
|  DDProductConsolidatorEngine  | 2237  | 0.000 | 21.235 | 208.768 | 27.446 |
| ComputeContainerRelatedEngine | 2084  | 0.000 | 1.969  | 14.856  | 1.686  |
|   ComputeCompletenessEngine   | 8135  | 0.000 | 0.100  |  2.890  | 0.169  |
|             Total             | 49435 |       |        |         |        |

### Conclusion

Grouping database interactions improved the load average of the database cluster and engine performances, enough to open the way to create a coding pattern around this and propagate it to other parts of the system.

## 1.14 Super U: propagating the learned lesson

Container attachment is a costly process that implied then single product queries during product consolidation, and single queries in container processing.

Container attachment will be separated from product consolidation to a dedicated engine, allowing a better bandwidth for the product engine.

Basic profiling has been done to identify some heavy CPU usage that could be easily optimized around data serialization.

### Actions

#### Global scope

- rationalize the use of DAO's to_dict method because of the necessary costly serialization

#### mass-model

- deserialization of Zulu date by using fromisoformat() rather than dateutils parser (this last one is dedicated to parsing with resilience, slow behavior expected)

#### maas-engine

- knowledge management: [performance guide with design and coding tips](https://gitlab2.telespazio.fr/maas/core/maas-engine/-/blob/develop/docs/performance_guide.md)
- [queue utilities](https://gitlab2.telespazio.fr/maas/core/maas-engine/-/blob/develop/docs/queue_utils.md) to solve chunk_size problems

#### maas-cds

- refactor of container engines to incorporate MultiSearch

### Effects

First deployment has seen an event that was not reproducible on pre-production means: the size of container payloads emitted by product consolidation implied a too large request time response on a very large data volume, provoking a loop of timeouts. Trials rarely come without errors.

Queues were filled, but reusable small utilities were developed to solve the problem by backing them up, modifying their chunk size and posting them back to the queues.

opensearch:

- load average decreased from 6 to 4
- max cpu usage increased from 50% to 60%

### Metrics

_Non-significant entries have been stripped but total kept_.

#### Duration summary in seconds

|             Engine             | Calls |  Min  |  Mean  |   Max   |  Std   |    Cum     |   %   |
| :----------------------------: | :---: | :---: | :----: | :-----: | :----: | :--------: | :---: |
|   ComputeCompletenessEngine    | 14206 | 0.005 | 18.328 | 121.519 | 15.988 | 260368.890 | 33.71 |
| PublicationConsolidatorEngine  | 19317 | 0.177 | 9.818  | 116.116 | 9.843  | 189663.058 | 24.56 |
|  LTAProductConsolidatorEngine  | 7608  | 0.188 | 12.736 | 94.695  | 12.262 | 96893.355  | 12.55 |
| ComputeContainerRelatedEngine  | 3724  | 0.199 | 15.720 | 46.698  | 7.687  | 58540.931  | 7.58  |
|  ComputeS3CompletenessEngine   |  880  | 0.014 | 57.521 | 296.756 | 59.229 | 50618.654  | 6.55  |
|   ProductConsolidatorEngine    | 8521  | 0.169 | 5.145  | 19.211  | 2.903  | 43838.456  | 5.68  |
| ComputeContainerProductsEngine | 5997  | 0.119 | 7.035  | 45.178  | 8.410  | 42186.941  | 5.46  |
|  ComputeS5CompletenessEngine   | 1040  | 0.016 | 13.973 | 104.615 | 16.714 | 14532.397  | 1.88  |
|  DDProductConsolidatorEngine   | 3187  | 0.226 | 3.867  | 37.187  | 2.795  | 12323.683  | 1.60  |
|             Total              | 85324 |       |        |         |        | 772338.454 |       |

#### Performance summary in document per second

|               Engine               | Calls |  Min  |  Mean  |   Max   |  Std   |
| :--------------------------------: | :---: | :---: | :----: | :-----: | :----: |
|     ProductConsolidatorEngine      | 8521  | 0.000 | 84.877 | 340.307 | 47.825 |
|   PublicationConsolidatorEngine    | 19317 | 0.096 | 48.612 | 243.756 | 36.307 |
|    LTAProductConsolidatorEngine    | 7608  | 0.000 | 46.125 | 296.151 | 43.944 |
|    DDProductConsolidatorEngine     | 3187  | 0.000 | 23.229 | 205.556 | 25.287 |
| DdpDataAvailableConsolidatorEngine |  608  | 1.189 | 20.361 | 75.000  | 12.976 |
|   ComputeContainerRelatedEngine    | 3724  | 0.000 | 7.452  | 20.703  | 3.413  |
|     ComputeCompletenessEngine      | 14206 | 0.000 | 0.085  |  2.890  | 0.167  |
|   ComputeContainerProductsEngine   | 5997  | 0.000 | 0.002  |  2.251  | 0.054  |
|               Total                | 85324 |       |        |         |        |

### Conclusion

Hopefully, round-robin queue consuming saved all other missions than S2 from experiencing data availability delay.
That proved that the externalization of heavy S2 process contained in product consolidation provided a better processing load for the whole mission set.

A hotfix has been rapidly deployed to mitigate chunk size of container messages sent from product consolidation and the queue occupation went then to a more than reasonable behavior.

## 1.15 Violette: engine pipeline optimization

With the perspective to add 4 LTA services to the system, the pipeline of two engines (publication and product) called for prip, lta and dd ingestion was the focused target.

### Actions

#### mass-model + maas-collector

- explicit index in payload to lower the use of alias

#### maas-engine

- EngineSession to share data between engines in a pipeline
- fill explicit index in generated payloads
- explicit index in payloads generated from reports

#### maas-cds

- Thanks to EngineSession, those tasks are executed only once per consolidation pipeline for publication-product queues (prip, lta, dd ...):
  - input documents loading
  - data extraction from product names
  - datatake attachment queries

### Effects

As publication engine already process all data dependencies, it shows only a little but promising improvement (explicit index on raw data), but the real improvement is that product engines and derivates are a lot faster.

### Metrics

_Non-significant entries have been stripped but total kept_.

#### Duration summary in seconds

|             Engine             | Calls |  Min  |  Mean  |   Max   |  Std   |    Cum     |   %   |
| :----------------------------: | :---: | :---: | :----: | :-----: | :----: | :--------: | :---: |
|   ComputeCompletenessEngine    | 16277 | 0.005 | 20.529 | 227.072 | 19.318 | 334153.981 | 46.18 |
| PublicationConsolidatorEngine  | 20170 | 0.176 | 7.138  | 121.696 | 8.409  | 143975.989 | 19.90 |
| ComputeContainerRelatedEngine  | 3599  | 0.367 | 14.806 | 68.043  | 8.746  | 53285.052  | 7.36  |
|   ProductConsolidatorEngine    | 8439  | 0.177 | 5.747  | 30.271  | 4.447  | 48502.027  | 6.70  |
| ComputeContainerProductsEngine | 5926  | 0.119 | 8.105  | 60.856  | 9.642  | 48031.790  | 6.64  |
|  LTAProductConsolidatorEngine  | 7772  | 0.181 | 4.315  | 27.225  | 3.133  | 33536.437  | 4.63  |
|  DDProductConsolidatorEngine   | 3959  | 0.157 | 3.340  | 17.410  | 2.187  | 13222.305  | 1.83  |
|             Total              | 93500 |       |        |         |        | 723562.797 |       |

#### Performance summary in document per second

|              Engine               | Calls |  Min  |  Mean  |   Max   |  Std   |
| :-------------------------------: | :---: | :---: | :----: | :-----: | :----: |
|     ProductConsolidatorEngine     | 8439  | 0.150 | 87.664 | 403.974 | 53.251 |
|   LTAProductConsolidatorEngine    | 7772  | 0.000 | 84.305 | 400.940 | 71.742 |
|   PublicationConsolidatorEngine   | 20170 | 0.000 | 53.543 | 350.205 | 41.950 |
|    DDProductConsolidatorEngine    | 3959  | 0.000 | 12.195 | 126.953 | 12.963 |
| InterfaceStatusConsolidatorEngine | 19050 | 0.176 | 9.331  | 23.256  | 4.555  |
|   ComputeContainerRelatedEngine   | 3599  | 0.217 | 8.766  | 20.566  | 3.962  |
|     ComputeCompletenessEngine     | 16277 | 0.000 | 0.072  |  3.311  | 0.159  |
|  ComputeContainerProductsEngine   | 5926  | 0.000 | 0.005  |  4.555  | 0.097  |
|               Total               | 93500 |       |        |         |        |

### Conclusion

The work about explicit index in messages was not fully completed: partitioning of consolidated products and publications is not naive. To secure the functional perimeter as it came late in the sprint, it has been delayed to the next sprint.

## 1.16 Werter's: lowering iops

### Actions

#### maas-cds

- explicit index for consolidated products and publications: reversible partitioning logic

### Effects

Being able to list the consolidated partitions for the highest volume demonstrate that using the alias of a set of indices relays the query for all the indices matching the pattern, resulting in a huge usage of iops.

As explicit naming is far faster, the whole cluster performances got better.

### Metrics

_Non-significant entries have been stripped but total kept_.

#### Duration summary in seconds

|             Engine             | Calls |  Min  |  Mean  |   Max   |  Std   |    Cum     |   %   |
| :----------------------------: | :---: | :---: | :----: | :-----: | :----: | :--------: | :---: |
|   ComputeCompletenessEngine    | 18113 | 0.004 | 14.838 | 142.544 | 13.473 | 268761.975 | 52.48 |
| PublicationConsolidatorEngine  | 22598 | 0.048 | 2.321  | 84.545  | 3.723  | 52459.241  | 10.24 |
| ComputeContainerRelatedEngine  | 3124  | 0.669 | 14.200 | 90.379  | 9.378  | 44360.743  | 8.66  |
| ComputeContainerProductsEngine | 5892  | 0.123 | 6.655  | 60.579  | 8.890  | 39209.267  | 7.66  |
|  LTAProductConsolidatorEngine  | 11019 | 0.176 | 3.015  | 62.146  | 2.617  | 33221.447  | 6.49  |
|   ProductConsolidatorEngine    | 8204  | 0.166 | 2.908  | 23.051  | 2.216  | 23854.220  | 4.66  |
|  DDProductConsolidatorEngine   | 3373  | 0.174 | 2.323  | 56.674  | 2.218  |  7834.229  | 1.53  |
|             Total              | 98691 |       |        |         |        | 512107.811 |       |

#### Performance summary in document per second

|              Engine               | Calls |  Min  |  Mean   |   Max   |   Std   |
| :-------------------------------: | :---: | :---: | :-----: | :-----: | :-----: |
|   PublicationConsolidatorEngine   | 22598 | 0.000 | 186.425 | 677.330 | 165.095 |
|     ProductConsolidatorEngine     | 8204  | 0.000 | 167.212 | 490.452 | 99.513  |
|   LTAProductConsolidatorEngine    | 11019 | 0.000 | 92.613  | 496.945 | 104.361 |
|    DDProductConsolidatorEngine    | 3373  | 0.000 | 24.941  | 323.735 | 31.169  |
| InterfaceStatusConsolidatorEngine | 20140 | 0.392 | 12.385  | 23.810  |  4.353  |
|   ComputeContainerRelatedEngine   | 3124  | 0.183 |  9.921  | 20.953  |  4.090  |
|     ComputeCompletenessEngine     | 18113 | 0.000 |  0.102  |  2.710  |  0.185  |
|  ComputeContainerProductsEngine   | 5892  | 0.000 |  0.001  |  1.923  |  0.037  |
|               Total               | 98691 |       |         |         |         |

## 1.17 Yeot

No code for performance has been written for this version.

## X.Y Sprint Name

_Template section for later sprints_.

### Actions

#### maas-cds

- (?) S1 completeness optimization
- (?) S2 completeness optimization
- (?) container linking by key

### Effects

TBW

### Metrics

_Non-significant entries have been stripped but total kept_.

#### Duration summary in seconds

TBW

#### Performance summary in document per second

TBW

### Conclusion

TBW

## Aftermath

Analyzing raw metrics only have sens in terms of tendency: how a set of patch affect a version ?

If strong metric variations are the first interesting facts, stability means also a lot: progress done in a sprint is kept in the next.

### Evolution of mean duration

|             Engine             | Tagada  |    Super U    |   Violette   |   Werter's   | Overall Delta | Overall Ratio |
| :----------------------------: | :-----: | :-----------: | :----------: | :----------: | :-----------: | :-----------: |
|   ComputeCompletenessEngine    | 19.469  |    18.328     |    20.529    |    14.838    |      N/A      |      N/A      |
| PublicationConsolidatorEngine  |  9.141  |     9.818     | 7.138 (-27%) | 2.321(-67%)  |     -75%      |     3.96      |
|   ProductConsolidatorEngine    | 29.095  | 5.145 (-82%)  |    5.747     | 2.908 (-49%) |     -90%      |     10.00     |
| ComputeContainerRelatedEngine  | 101.878 | 15.720 (-84%) |    14.806    |    14.200    |     -86%      |     7.17      |
| ComputeContainerProductsEngine |   N/A   |     7.035     |    8.105     |    6.655     |      N/A      |      N/A      |
|  LTAProductConsolidatorEngine  | 11.782  |    12.736     | 4.315 (-66%) |    3.015     |     -74%      |     3.91      |
|  DDProductConsolidatorEngine   |  3.115  |     3.867     |    3.340     |    2.323     |     -25%      |     1.34      |

Publication and LTA consolidation engines are close to four times more efficient, so hosting four more LTA may not have too many risks.

### Evolution of max duration

_Beware: these are the worst cases that may depend on external interfaces behavior._

|             Engine             | Tagada  |    Super U     |   Violette    |   Werter's    | Overall Delta | Overall Ratio |
| :----------------------------: | :-----: | :------------: | :-----------: | :-----------: | :-----------: | :-----------: |
|   ComputeCompletenessEngine    | 134.530 |    121.519     |    227.072    |    142.544    |      N/A      |      N/A      |
| PublicationConsolidatorEngine  | 139.929 | 116.116 (-17%) |    121.696    | 84.545 (-30%) |     -39%      |     1.65      |
|   ProductConsolidatorEngine    | 491.838 | 19.211 (-96%)  |    30.271     | 23.051 (-23%) |     -95%      |     21.34     |
| ComputeContainerRelatedEngine  | 544.548 | 46.698 (-91%)  |    68.043     |    90.379     |     -83%      |     6.02      |
| ComputeContainerProductsEngine |   N/A   |     45.178     |    60.856     |    60.579     |      N/A      |      N/A      |
|  LTAProductConsolidatorEngine  | 131.201 | 94.695 (-27%)  | 27.225 (-71%) |    62.146     |     -52%      |     2.11      |
|  DDProductConsolidatorEngine   | 16.241  |  3.867 (-76%)  |     3.340     |    56.674     |               |               |

### Evolution of CPU cumulated time percentage

This metrics represents a kind of cluster weather: what is the cluster, and what are the usages of the engines ?

Increased proportion does not mean at all that an engine is slower: it's because all other things run faster and offer more CPU time for this engine.

This can be verified by correlating the proportion delta with the stability of mean duration of engine runs.

Overall it can be considered

|             Engine             | Tagada |   Super U    |   Violette   |   Werter's   | Overall Delta | Overall Ratio |
| :----------------------------: | :----: | :----------: | :----------: | :----------: | :-----------: | :-----------: |
|   ProductConsolidatorEngine    | 21.46  | 5.68 (-73%)  | 6.70 (+17%)  | 4.66 (-30%)  |     -78%      |     4.61      |
| PublicationConsolidatorEngine  | 15.88  | 24.56 (+54%) | 19.90 (-18%) | 10.24 (-48%) |     -35%      |     1.55      |
|  LTAProductConsolidatorEngine  |  8.38  | 12.55 (+33%) | 4.63 (-63%)  | 6.49 (+40%)  |     -22%      |     1.29      |
|  DDProductConsolidatorEngine   |  0.90  |     1.60     |     1.83     |     1.53     |      N/A      |      N/A      |
|   ComputeCompletenessEngine    | 20.45  | 33.71 (+64%) | 46.18 (+37%) | 52.48 (+14%) |     +156%     |     0.38      |
| ComputeContainerRelatedEngine  | 27.41  | 7.58 (-72%)  |     7.36     |     8.66     |     -68%      |     3.17      |
| ComputeContainerProductsEngine |  N/A   |     5.46     |     6.64     |     7.66     |      N/A      |      N/A      |

### Evolution of mean document per second

|             Engine             | Tagada |    Super U    |   Violette    |    Werter's    | Overall Delta | Overall Ratio |
| :----------------------------: | :----: | :-----------: | :-----------: | :------------: | :-----------: | :-----------: |
|   ProductConsolidatorEngine    | 43.520 | 84.877 (+95%) |    87.664     | 167.212 (+88%) |     +284%     |     3.84      |
| PublicationConsolidatorEngine  | 49.489 |    48.612     |    53.543     |    186.425     |     +276%     |     3.76      |
|  LTAProductConsolidatorEngine  | 48.827 |    46.125     | 84.305 (+82%) |     92.613     |     +89%      |     1.89      |
|  DDProductConsolidatorEngine   | 21.235 |    23.229     |    12.195     |     24.941     |     +17%      |     1.17      |
|   ComputeCompletenessEngine    |  0.1   |     0.085     |     0.072     |     0.102      |      N/A      |      N/A      |
| ComputeContainerRelatedEngine  | 1.969  | 7.452 (+278%) |     8.766     |     9.921      |     +403%     |     5.03      |
| ComputeContainerProductsEngine |  N/A   |     0.002     |     0.072     |     0.001      |      N/A      |      N/A      |

### Evolution of max document per second

|             Engine             | Tagada  |    Super U     |    Violette    | Werter's | Overall Delta | Overall Ratio |
| :----------------------------: | :-----: | :------------: | :------------: | :------: | :-----------: | :-----------: |
|   ProductConsolidatorEngine    | 287.479 | 340.307 (+18%) | 403.974 (+18%) | 490.452  |     +70%      |     1.71      |
| PublicationConsolidatorEngine  | 204.880 | 243.756 (+18%) | 350.205 (+43%) | 677.330  |     +230%     |     3.30      |
|  LTAProductConsolidatorEngine  | 252.715 | 296.151 (+17%) | 400.940 (+35%) | 496.945  |     +96%      |     1.96      |
|  DDProductConsolidatorEngine   | 208.768 |    205.556     |    126.953     | 323.735  |     +54%      |     1.55      |
|   ComputeCompletenessEngine    |  2.890  |     2.890      |     3.311      |  2.710   |      N/A      |      N/A      |
| ComputeContainerRelatedEngine  |  1.969  | 20.703 (+951%) |     20.566     |  20.953  |     +964%     |     10.64     |
| ComputeContainerProductsEngine |   N/A   |     2.251      |     4.555      |  1.923   |      N/A      |      N/A      |
