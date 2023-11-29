# maas-cds

OMCS data implementation: an ETL built with maas-engine.

## Using container to generate CDS models

Generate collector configuration file for CDS model matching opensearchemplates:

```bash
docker pull tpzf-ssa-docker-registry:5000/maas/maas-cds:latest
docker run -it --rm tpzf-ssa-docker-registry:5000/maas/maas-cds:latest /app/scripts/generate-collector-model-conf.sh | grep -v "^INFO" > generated-model.json
```

Generate collector configuration file for generic model matching local opensearchpy templates:

```bash
docker pull tpzf-ssa-docker-registry:5000/maas/maas-cds:latest
docker run -it --rm -v $PWD/templates:/app/resources/templates tpzf-ssa-docker-registry:5000/maas/maas-cds:latest /app/scripts/generate-collector-model-conf.sh | grep -v "^INFO" > generated-model.json
```

## Update Public Dashboard data

Public Dashboard reads data from a S3 bucket.

`maas-cds` provides the cli utility `maas_update_public_site` that queries opensearchpy database and upload reports to a S3 bucket. It requires a `maas-engine` configuration file (located in maas-deploy-cds/configuration/engines/export/cds-engine-conf.json) and requires the standard `maas-engine` options plus the following to declare the S3 bucket:

```
 --s3-endpoint S3_ENDPOINT
                        S3 endpoint URL (default: None)
  --s3-key-id S3_KEY_ID
                        S3 key identifier (default: None)
  --s3-access-key S3_ACCESS_KEY
                        S3 access key (default: None)
  --s3-bucket S3_BUCKET
                        S3 bucket (default: None)
```

Additionally, the following options are useful for development and debug:

```
  -d, --dryrun          Do not upload data
  --output-dir OUTPUT_DIR
                        Save files to a local directory
```

## El_Grando_Satruman usage

- Usage

```bash
usage: el_grando_satruman [-h] [--es-username ES_USERNAME] [--es-password ES_PASSWORD] [--es-url ES_URL] [--es-timeout ES_TIMEOUT] [--es-retries ES_RETRIES] [--es-reject-errors]
                          [--amqp-username AMQP_USERNAME] [--amqp-password AMQP_PASSWORD] [--amqp-url AMQP_URL] [--amqp-retries AMQP_RETRIES] [--amqp-max-priority AMQP_MAX_PRIORITY]
                          [--amqp-priority AMQP_PRIORITY] [--chunk-size CHUNK_SIZE] [-v] [-vv] [-c CONFIG] [--document-class DOCUMENT_CLASS] [--routing-key ROUTING_KEY] [--query-string QUERY_STRING]
                          [--operation OPERATION] [--operation-args OPERATION_ARGS] [-d]
```

- Concret args usage

  - Operation  
    --operation OPERATION : The operation engine id  
    --operation-args OPERATION_ARGS : The operations payload need by the target operation engine

  - Query engine  
    --document-class DOCUMENT_CLASS : The class document name of the target entity (ie: for cds-product indices use CdsProduct)  
    --routing-key ROUTING_KEY : The routing key on which to distribute the messages (if it is not provided it is the one associated with the document class ie: CdsProduct -> etl-update.cds-product)  
    --query-string QUERY_STRING : The query string to refine the targeting

  - Common args  
    -d, --dry-run : Dry run no data update / no message send
    --chunk-size : How many target entities by message
    --amqp-priority : The message priority (usefull for quick processing or low priority)
    ...args : Other args aiming es/amqp mainly provided by ENV_VAR

### Query engine (No operation provided)

- Base

  ```bash
  $DOCUMENT_CLASS=""
  $ROUTING_KEY=""
  $QUERY_STRING=""

  el_grando_satruman --document-class $DOCUMENT_CLASS --routing-key $ROUTING_KEY --query-string $QUERY_STRING -v
  ```

- Concret usecase:

  - To retrieve MSI_L1C_DS to relaunch expected tiles evaluation by computing completeness on associate datatake

    ```bash
    el_grando_satruman --document-class CdsProductS2 --routing-key compute.cds-datatake --query-string "sensing_start_date: [2022-12-01 TO 2022-12-31] AND product_type: MSI_L1C_DS" -v --chunk-size 128
    ```

### Operation Missing Consolidation

- Base

  ```bash
  $SERVICE_TYPES=[]
  $SERVICE_IDS=[]
  $QUERY_STRING=""

  el_grando_satruman --operation "missing_consolidation" --operation-args '{"service_types": $SERVICE_TYPES, "service_ids": $SERVICE_IDS,"query_string": $QUERY_STRING"}' -v
  ```

- Concret usecase:

  - To retrieve DHUS container not consolidated on a given period

    ```bash
    el_grando_satruman --operation "missing_consolidation" --operation-args '{"service_types": ["DD"], "service_ids":["DHUS"],"query_string": "product_name: S2*MSI*L1* AND start_date: [2022-12-10T20:54:48 TO 2022-12-10T20:55:10]"}' -v
    ```

  - To retrieve S5P product not consolidated on a given period for all services

    ```bash
    el_grando_satruman --operation "missing_consolidation" --operation-args '{"service_types": ["DD", "LTA", "PRIP"],"query_string": "ingestionTime: [2022-11-08T00:00:00.000Z TO 2022-11-22T00:00:00.000Z] AND product_name: S5P_*"}
    ```

  - To retrieve product not consolidated after earlier collector restart

    ```bash
    el_grando_satruman --operation "missing_consolidation" --operation-args '{"service_types": ["DD"],"query_string": "ingestionTime: [2023-01-26T13:55:00.000Z TO 2023-01-26T14:10:00.000Z]"}' -v --chunk-size 128
    ```
