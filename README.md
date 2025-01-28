# Omcs Installation and running

Omcs is a complete solution for monitoring process, it's based on microservices to collect, compute and display monitoring informations.
It uses several components:

- Elasticsearch (Opendistro) for data storage.
- Grafana for data display.
- RabbitMq for communication between components.
- MAAS-Collector for data collection.
- MAAS-CDS ( based on MAAS-Engine) for data computation

It depends on Python:

- Python 3.11 as MAAS-XXXX is coded in python

## Install

### Get the sources

Sources are available on [GitHub](https://github.com/coordinationdesk/end2end_monitoring_dashboard).

```bash
git clone https://github.com/coordinationdesk/end2end_monitoring_dashboard.git
cd ./end2end_monitoring_dashboard
```

### Folder organization

- ${WORK_DIR}
  - development
  - cots
  - data
    - reports
  - deployment
    - charts
    - configuration
      - collector
      - credentials
      - engine
      - grafana
    - docs
    - templates
    - values
  - docs
  - logs
  - modules
    -build
    - maas-cds
      - maas-collector
      - maas-engine
      - maas-model
  - scripts

### Environement preparation

Update, correct and source your environement.

Environement variables needed:

- PYTHON_VERSION="3.11"
- WORK_DIR="PATH/TO/THE/PROJECT/FOLDER"
- LOGS_DIR="PATH/TO/THE/LOGS"
- VENV_NAME="phyton virtual environement name (omcs-venv)
- VENV_PATH="="PATH/TO/THE/VENV"
- ES_USERNAME="the user name for opensearch access"
- ES_PASSWORD="the user password for opensearch access"
- ES_PORT="the opensearch port"
- ES_URL="the opensearch url"
- AMQP_USERNAME="the user name for rabbitmq access"
- AMQP_PASSWORD="the user password for rabbitmq access"
- AMQP_PORT="the rabbitmq port"
- AMQP_URL="the rabbitmq url"
- AMQP_IHM_PORT="the rabbitmq http monitoring port"
- GRF_PORT="the grafana port"
- HEALTHCHECK_HOSTNAME="Ports for health check"
- INITDB_HEALTH_PORT="Ports for health check"
- ENGINE_HEALTH_PORT="Ports for health check"
- COLLECTOR_HEALTH_PORT="Ports for health check"

Update env.sh file with your values and source it.

```bash
source ./scripts/env.sh
```

All needed variables will be sourced and displayed in order to be checked.

As already mentionned, scripts use Python. It will be usefull to create and source a python virtual environement.

```bash
python3.11 -m venv "${VENV_PATH}"
source ${VENV_PATH}/bin/activate
```

### Cots used

All COTS are used as docker containers and could be organized in a docker-compose file:

```bash
cat ${WORK_DIR}/docker-compose.yaml
```

To launch COTS use `docker-compose`commands:

```bash
docker-compose -f ${WORK_DIR}/docker-compose.yaml up -d
```

### maas components

Maas components are Python modules encapsulated in docker containers.

Python module "wheels" files (.whl) could be retrieved in [releases](https://github.com/coordinationdesk/end2end_monitoring_dashboard/releases), or built from module sources.

Docker containers are built using docker builds and DockerFile.

- maas-cds uses ./modules/DockerFile.cds
- maas-collector uses ./modules/DockerFile.collector

#### Get wheel from release

From [releases](https://github.com/coordinationdesk/end2end_monitoring_dashboard/releases) download wheel files (*.whl) into ./modules/build/<module_name>/module.whl .

ex : cp maas_cds-1.0.0-py2.py3-none-any.whl ./modules/build/maas_cds/maas_cds-1.0.0-py2.py3-none-any.whl

Then jump to step : [Build docker images](./README.md#build-docker-images).

To build them by yourself adapt and use the given scripts.

#### build from modules sources

Maas components are Python modules. They should be built and installed using pip.

First, install Python 3.11; pip should be installed on the destination server.

Define a virtual env for maas components.

```bash
python${PYTHON_VERSION} -m venv ${WORK_DIR}/omcs-venv-${PYTHON_VERSION}
source ${WORK_DIR}/omcs-venv-${PYTHON_VERSION}/bin/activate
```

- Either, install locally Maas components Python modules using pip.

```bash
pip install -e ${WORK_DIR}/maas-model/
pip install -e ${WORK_DIR}/maas-engine/
pip install -e ${WORK_DIR}/maas-collector/
pip install -e ${WORK_DIR}/maas-cds/
```

Or adapt and use use given script.

```bash
${WORK_DIR}/scripts/local_install.sh
```

To build python "wheel" files use tox command:

```bash
tox -c ${WORK_DIR}/maas-model/tox.ini -e build
tox -c ${WORK_DIR}/maas-engine/tox.ini -e build
tox -c ${WORK_DIR}/maas-collector/tox.ini -e build
tox -c ${WORK_DIR}/maas-cds/tox.ini -e build
```

Or adapt and use use given script.

```bash
${WORK_DIR}/scripts/build_modules.sh
```

#### Build docker images

To build docker images use docker build commands.
To get git tag version use git command:

```bash
docker build -t "maas-collector:${COLLECTOR_TAG_VERSION}" -f "${WORK_DIR}/modules/Dockerfile.maas-collector" ./modules
docker build -t "maas-cds:${CDS_TAG_VERSION}" -f "${WORK_DIR}/modules/Dockerfile.maas-cds" ./modules
```

Or adapt and use use given script.

```bash
${WORK_DIR}/scripts/build_dockers.sh
```

## Configure MAAS

Some configuration should be set for MAAS usage:

### Grafana

Dashboards and datasources should be set for Grafana.

They are delivered on the Github.

You could find them in the following folder:

```bash
ls -al ${WORK_DIR}/deployment/configuration/grafana
```

### MAAS-engine

The maas engine need configuration this omcs specific configuration.

They are delivered in the github.

You could find them in the following folder:

```bash
ls -al ${WORK_DIR}/deployment/configuration/engines/cds-engine-conf.json
```

### MAAS-collector

The maas engine need configuration this omcs specific configuration.

They are delivered in the github.

You could find them in following folder:

```bash
ls -al ${WORK_DIR}/deployment/configuration/collector/
```

### Credentials

The Maas-collector needs to collect external interfaces credentials.

They are not deliverded in Github, only a sample file is provided. 
Please note that correct values should be set:

```bash
ls -al ${WORK_DIR}/deployment/configuration/credentials/maas-api-collector-credentials.json
```

## Launch MAAS

### Start COTS

To start the application COTS use docker-compose command:

```bash
docker-compose -f ${WORK_DIR}/docker-compose.yaml up -d
```

The service could be found here:

- [elasticsearch](https://localhost:9200) (admin:admin)
- [rabbitmq](http://localhost:15672) (guest:guest)
- [grafana](http://localhost:3000)

Check that the database is running with the following cmd:

```bash
curl -k https://<user_name>:<user_passwd>@localhost:${ES_PORT}/"
```

### Init the database (only at first launch)

The database init is launched using a simple shell command. See the documentation for needed arguments.

```bash
TZ=UTC maas_migrate -v --es-ignore-certs-verification True -r ${WORK_DIR}/maas-cds/resources/ --install all &
```

### Engine

#### from local install

The engine is launched using a simple shell command. See the documentation for needed arguments.
There will be consolidated data on collect events.

```bash
TZ=UTC python -m maas_engine -v --es-ignore-certs-verification True -c ${WORK_DIR}/deployment/configuration/engines/cds-engine-conf.json -f --healthcheck-port ${ENGINE_HEALTH_PORT}
```

#### using docker image

You can use a docker run command to launch maas-cds engine:

```bash
docker run -it --rm -v "${PWD}/deployment/configuration/:/conf" \
-e "ES_USERNAME=${ES_USERNAME}" \
-e "ES_PASSWORD=${ES_PASSWORD}" \
-e "ES_PORT=${ES_PORT}" \
-e "ES_URL=${ES_URL}" \
-e "AMQP_PORT=${AMQP_PORT}" \
-e "AMQP_IHM_PORT=${AMQP_IHM_PORT}" \
-e "AMQP_URL=${AMQP_URL}" \
-e "AMQP_USERNAME=${AMQP_USERNAME}" \
-e "AMQP_PASSWORD=${AMQP_PASSWORD}" \
--network host \
maas-cds:${CDS_TAG_VERSION}  maas_engine -v --es-ignore-certs-verification True -c "/conf/engine/cds-engine-conf.json"
```

### Collector

The collector is launched using a simple shell command. See the documentation for needed arguments.

#### Collect in local folder

Using reports as files on local filesystem, the collector will retrieve reports and collect them.

```bash
TZ=UTC python -m maas_collector.rawdata.cli.filesystem -v --es-ignore-certs-verification True -d ${WORK_DIR}/deployment/configuration/collector/ --healthcheck-port ${COLLECTOR_HEALTH_PORT} ${WORK_DIR}/data/reports -p 0 -f
```

#### Collect external services

Using severals external api here odata the collector will query the service and collect responces.

```bash
TZ=UTC python -m maas_collector.rawdata.cli.odata -v --es-ignore-certs-verification True -d ${WORK_DIR}/deployment/configuration/collector/ --healthcheck-port ${COLLECTOR_HEALTH_PORT} --credential-file ${WORK_DIR}/deployment/configuration/credentials/maas-api-collector-credentials.json -p 0 -f &
```

#### Collect locally using a docker image

You can use a docker run command to launch maas-collector:

```bash
docker run -it --rm -v "${PWD}/data/:/data" \
-v "${PWD}/deployment/configuration/:/conf" \
-e "ES_USERNAME=${ES_USERNAME}" \
-e "ES_PASSWORD=${ES_PASSWORD}" \
-e "ES_PORT=${ES_PORT}" \
-e "ES_URL=${ES_URL}" \
-e "AMQP_PORT=${AMQP_PORT}" \
-e "AMQP_IHM_PORT=${AMQP_IHM_PORT}" \
-e "AMQP_URL=${AMQP_URL}" \
-e "AMQP_USERNAME=${AMQP_USERNAME}" \
-e "AMQP_PASSWORD=${AMQP_PASSWORD}" \
--network host \
maas-collector:${COLLECTOR_TAG_VERSION} maas_collector.rawdata.cli.filesystem -v --es-ignore-certs-verification True -d "/conf/collector/" -f "/data"
```

## Deployment

Omcs could be deployed on the "cloud". To do it, you will be guided by reading the [deployment](./deployment/docs/deployment.md) documentation.


## CI/CD


https://adamj.eu/tech/2023/11/02/github-actions-faster-python-virtual-environments/
