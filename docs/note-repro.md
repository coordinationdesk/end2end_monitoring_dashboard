# Note Repro

For business reasons, we had to ingest products from reprocessing (hence the repro) services.
We chose to have a different MaaS instance (the volumes announced were too large to guarantee stability with the initial elastic cluster, and the application code), with dedicated resources to avoid impacting nominal production, as these data potentially have different life cycles. This isolation avoids side-effects on nominal production. And allocated resources can also be used by nominal production, with a lower priority.

To easily identify these resources, the suffix repro is used.

At the beginning, we had two grafana; due to totally different infrastructures, following a migration on the same infrastructure, we decided to mutualize the grafana and the monitoring.
