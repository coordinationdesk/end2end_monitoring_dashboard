# Development

## Setup

```bash
# Adjust here if needed
export WORK_DIR=~/work/end2end_monitoring_dashboard
source $WORK_DIR/development/.env

python${PYTHON_VERSION} -m venv ${WORK_DIR}/omcs-venv-${PYTHON_VERSION}-dev
source ${WORK_DIR}/omcs-venv-${PYTHON_VERSION}-dev/bin/activate
```

## Launch cots

```bash
docker compose -f ${WORK_DIR}/development/docker-compose.yaml --env-file ${WORK_DIR}/development/.env up -d 
```

Verify database setup

```bash
curl $ES_URL  -k -u $ES_USERNAME:$ES_PASSWORD
```

Verify grafana provissioning at `http://localhost:${GRF_PORT}/dashboards`
and `http://localhost:${GRF_PORT}/connections/datasources`

Verify RMQ launch at http://localhost:${AMQP_IHM_PORT}/

## Install module locally

Go inside all module and install it locally

May need some python packages

```bash
pip install --upgrade pip
pip install -U setuptools setuptools_scm wheel
pip install -U tox
```

Then perform local maas install

```bash
cd $WORK_DIR/modules/maas-model/
pip install -e .
cd $WORK_DIR/modules/maas-engine/
pip install -e .
cd $WORK_DIR/modules/maas-cds/
pip install -e .
cd $WORK_DIR/modules/maas-collector/
pip install -e .
```

Verify the correct local installations

```bash
pip freeze | grep maas-
# Output look like
# -e git+ssh://REPO_REF#egg=maas_cds&subdirectory=modules/maas-cds
# -e git+ssh://REPO_REF#egg=maas_collector&subdirectory=modules/maas-collector
# -e git+ssh://REPO_REF#egg=maas_engine&subdirectory=modulesmaas-engine
# -e git+ssh://REPO_REF#egg=maas_model&subdirectory=modules/maas-model
```

## Setup database mapping

Before the first run you need to init mapping in the database

```bash
maas_migrate -v --install all -r $WORK_DIR/modules/maas-cds/resources
```

Then to check the correct init

```bash
curl ${ES_URL}cds-datatake-s1-s2 -k -u $ES_USERNAME:$ES_PASSWORD
```

## Load some data from aother cluster

This will depend of cours of how both cluster is configured

{
  "source": {
    "remote": {
      "host": "https://HOST:PORT",
      "username": "USER",
      "password": "PASSWORD"
    },
    "index": "raw-data-mp-product"
  },
  "dest": {
    "index": "raw-data-mp-product"
  }
}

### Host not allowed

```json
{
  "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "[HOST:PORT] not allowlisted in reindex.remote.allowlist"
      }
    ],
    "type": "illegal_argument_exception",
    "reason": "[HOST:PORT] not allowlisted in reindex.remote.allowlist"
  },
  "status": 400
}
```

In the opensearch config add the following

```yaml
reindex.remote.whitelist: ["HOST:PORT"]
```

if not inside a volume:
```bash
# Import file locally
docker cp dev-omcs-opensearch:/usr/share/opensearch/config/opensearch.yml $WORK_DIR/development/opensearch/opensearch.yml
# Edit as suggested
# Load file inside container
docker cp $WORK_DIR/development/opensearch/opensearch.yml dev-omcs-opensearch:/usr/share/opensearch/config/opensearch.yml
```

Then reload 
```bash 
docker restart dev-omcs-opensearch
```

### Add certificate

Error 

```json
{
  "error": {
    "root_cause": [
      {
        "type": "s_s_l_handshake_exception",
        "reason": "PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target"
      }
    ],
    "type": "s_s_l_handshake_exception",
    "reason": "PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target",
    "caused_by": {
      "type": "validator_exception",
      "reason": "PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target",
      "caused_by": {
        "type": "sun_cert_path_builder_exception",
        "reason": "unable to find valid certification path to requested target"
      }
    }
  },
  "status": 500
}
```

```bash
# First load the certificate inside the container
# You can also use volume
docker cp $WORK_DIR/development/opensearch/opensearch_certificate.der dev-omcs-opensearch:/tmp/opensearch_certificate.der

# Then go inside the container
docker exec -it dev-omcs-opensearch /bin/bash
keytool -importcert -alias mycert -file /tmp/opensearch_certificate.der -keystore $JAVA_HOME/lib/security/cacerts
# Type yes if information are good


# Then reload opensearch
docker restart dev-omcs-opensearch
```


### Bypass Certficate not match


Error 

```json
{
  "error": {
    "root_cause": [
      {
        "type": "s_s_l_peer_unverified_exception",
        "reason": "Host name 'HOST' does not match the certificate subject provided by the peer (CN=cert_HOST, OU=******, O=******, L=******, ST=******, C=******)"
      }
    ],
    "type": "s_s_l_peer_unverified_exception",
    "reason": "Host name 'HOST' does not match the certificate subject provided by the peer (CN=cert_HOST, OU=******, O=******, L=******, ST=******, C=******"
  },
  "status": 500
}
```

In docker compose add some extra host in the service

```yaml
    extra_hosts: 
      - "cert_HOST:real_HOST"
```

Next you will probably the same error as the beginning 
so add the cert_HOST:PORT in reindex.remote.whitelist: ["HOST:PORT"] as describe previously


Then update also the query

```json
{
  "source": {
    "remote": {
      "host": "https://cert_HOST:PORT",
      "username": "USER",
      "password": "PASSWORD"
    },
    "index": "raw-data-mp-product"
  },
  "dest": {
    "index": "raw-data-mp-product"
  }
}
```

## Run local python module

## Build local python wheel 

tox -c ./modules/maas-model/tox.ini -e build
cp -ar ${WORK_DIR}/modules/maas-model/dist/ ${WORK_DIR}/modules/build/maas-model/

tox -c ./modules/maas-engine/tox.ini -e build
cp -ar ${WORK_DIR}/modules/maas-engine/dist/ ${WORK_DIR}/modules/build/maas-engine/

tox -c ./modules/maas-collector/tox.ini -e build
cp -ar ${WORK_DIR}/modules/maas-collector/dist/ ${WORK_DIR}/modules/build/maas-collector/

tox -c ./modules/maas-cds/tox.ini -e build
cp -ar ${WORK_DIR}/modules/maas-cds/dist/ ${WORK_DIR}/modules/build/maas-cds/

## Build local docker image

```
docker build --no-cache -t "maas-cds:2.8.1-beta" -f ./modules/Dockerfile.maas-cds ./modules
docker build --no-cache -t "maas-collector:3.8.2-beta" -f ./modules/Dockerfile.maas-collector ./modules
```

## S3 bucket snapshot

```bash
docker exec -it dev-omcs-opensearch /bin/bash -c "opensearch-plugin install repository-s3"  
```


```bash
export S3_SECRET_KEY=""
export S3_ACCESS_KEY=""

docker exec -it dev-omcs-opensearch /bin/bash -c "opensearch-keystore list ; opensearch-keystore remove s3.client.default.access_key ;opensearch-keystore remove s3.client.default.secret_key; echo ${S3_ACCESS_KEY} | opensearch-keystore add --stdin --force s3.client.default.access_key && echo ${S3_SECRET_KEY} | opensearch-keystore add --stdin --force s3.client.default.secret_key; opensearch-keystore list"
```


## Performing some reprocessing


### Replay PRIP ingestion

```bash
el_grando_satruman --document-class PripProduct --query-string "interface_name: PRIP_S1C_Serco" --routing-key "new.raw.data.prip-product" --chunk-size "512" --amqp-priority 4 --output-document-class 'PripProduct' -c $WORK_DIR/development/maas-engine-conf/cds-engine.json

el_grando_satruman --document-class PripProduct --query-string "interface_name: PRIP_S1C_Werum" --routing-key "new.raw.data.prip-product" --chunk-size "512" --amqp-priority 4 --output-document-class 'PripProduct' -c $WORK_DIR/development/maas-engine-conf/cds-engine.json
```

### Compute again completeness S1 from completeness

```bash
el_grando_satruman --document-class CdsCompletenessS1 --query-string "sensing_global_percentage: [* TO 99] AND  observation_time_start: [now-7d TO now-2h]" --routing-key "compute.cds-completeness" --chunk-size "1" --amqp-priority 4 --output-document-class 'CdsCompletenessS1' -c $WORK_DIR/development/maas-engine-conf/cds-engine.json
```


## Replay RabbitMQ Manually

Some engine can't be trigger be satruman

#### collect-exchange

##### file.raw.data.mp-product


```json
{"date": "2025-01-20T13:43:32.773Z", "message_id": "49af7c48-d31b-45ef-8c3e-70d88d5f6271", "ancestor_ids": [], "pipeline": ["ODataCollector"], "force": true, "document_ids": ["S1C_MP_ACQ__L0__20250120T174545_20250124T181805.csv"], "document_indices": [], "document_class": "MpProduct"}
```

## Tips


- In this file all command are full, we encourage you to use aliases

### OpenSearch

For better OpenSearch explorations and manipulations https://elasticvue.com


Check Opensearch log `docker logs dev-omcs-opensearch`
With follow `docker logs -f dev-omcs-opensearch`

It's not possible to restore a snapshot from a higher version cluster.
However, it is possible to restore a snasphot from a lower version cluster (cool for upgrade).

For small extract you can use Elastic dump https://github.com/elasticsearch-dump/elasticsearch-dump
