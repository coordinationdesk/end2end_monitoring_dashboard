# Omcs Installation and running

Omcs is a complete solution for monitoring process, it's based on microservices to collect, compute and display monitoring information.
It uses several components:

- Elasticsearch (Opendistro) for data storage.
- Grafana for data display.
- RabbitMq for communication between components.
- MAAS-Collector for data collection.
- MAAS-CDS (based on MAAS-Engine) for data computation.

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
	- data
		- reports
	- deployment 
		- charts
		- configuration
			- grafana
			- engines
			- collector
				- collector
				- credentials
		- templates
		- values
	- modules
		- maas-cds
  		- maas-collector
  		- maas-engine
  		- maas-model

### Environement preparation

Update, correct and source your environement.

Environement variables needed:

- PYTHON_VERSION="3.11"
- WORK_DIR="PATH/TO/THE/PROJECT/FOLDER"
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

Or update env.sh file and source it.

```bash
source env.sh
```

### Cots

All cots are used as docker containers and could be organized in a docker-compose file:

```bash
cat ${WORK_DIR}/docker-compose.yaml
```

To launch cots use `docker-compose`commands:

```bash
docker-compose -f ${WORK_DIR}/docker-compose.yaml up -d
```

### maas components

Maas components are python modules encapsulated in docker containers.

Python modules wheel could be retrieved in [releases](https://github.com/coordinationdesk/end2end_monitoring_dashboard/releases), or build from modules sources.

Docker containers are built using docker builds and DockerFile.

- maas-cds uses ./modules/DockerFile.cds
- maas-collector uses ./modules/DockerFile.collector

#### Get wheel from release

From [releases](https://github.com/coordinationdesk/end2end_monitoring_dashboard/releases) download wheel files (*.whl) into ./modules/build/<module_name>/.

Jump to step : [Build docker images](./README.md#build-docker-images).

Or adapt and use the given script.

#### build from modules sources

Maas components are python modules, they should be built and installed using pip.

First python 3.11 and pip should be installed on the destination server.

Define a virtual env for maas components.

```bash
python${PYTHON_VERSION} -m venv ${WORK_DIR}/omcs-venv-${PYTHON_VERSION}
source ${WORK_DIR}/omcs-venv-${PYTHON_VERSION}/bin/activate
```

Install locally maas components and python modules using pip.

```bash
pip install -e ${WORK_DIR}/maas-model/
pip install -e ${WORK_DIR}/maas-engine/
pip install -e ${WORK_DIR}/maas-collector/
pip install -e ${WORK_DIR}/maas-cds/
```

Or adapt and use use the given script.

```bash
./local_install.sh
```

To build wheel uses tox command:

```bash
tox -c ${WORK_DIR}/maas-model/tox.ini -e build
tox -c ${WORK_DIR}/maas-engine/tox.ini -e build
tox -c ${WORK_DIR}/maas-collector/tox.ini -e build
tox -c ${WORK_DIR}/maas-cds/tox.ini -e build
```

Or adapt and use the given script.

```bash
./build_modules.sh
```

#### Build docker images

To build docker images, use docker build commands.
To get git tag version, use git command:

```bash
docker build -t "maas-collector:${COLLECTOR_TAG_VERSION}" -f "${WORK_DIR}/modules/Dockerfile.maas-collector" ./modules
docker build -t "maas-cds:${CDS_TAG_VERSION}" -f "${WORK_DIR}/modules/Dockerfile.maas-cds" ./modules
```

Or adapt and use the given script.

```bash
./docker_build.sh
```


## Configure MAAS

Some configuration should be set for MAAS usage:

### Grafana

Dashboards and datasources should be set for Grafana.

They are delivered in the github.

You could find them in the following folder:

```bash
ls -al ${WORK_DIR}/deployment/configuration/grafana
```

### MAAS-engine

The maas engine needs configuration. It is omcs specific configuration.

It is delivered in the github.

You could find them in the following folder:

```bash
ls -al ${WORK_DIR}/deployment/configuration/engines/cds-engine-conf.json
```

### MAAS-collector

The maas engine needs configuration. It is omcs specific configuration.

It is delivered in the github.

You could find them in the following folder:

```bash
ls -al ${WORK_DIR}/deployment/configuration/collector/
```

### Credentials

The maas collector needs to collect external interfaces and credential files.

They are not deliverded in github, however, a sample file is delivered. Correct values should be set in this file:

```bash
ls -al ${WORK_DIR}/deployment/configuration/credentials/maas-api-collector-credentials.json
```

## Launch MAAS

### Cots

To start the application cots, use docker-compose command:

```bash
docker-compose -f ${WORK_DIR}/docker-compose.yaml up -d
```

Service could be found here:

- [elasticsearch](https://localhost:9200) (admin:admin)
- [rabbitmq](http://localhost:15672) (guest:guest)
- [grafana](http://localhost:3000)


Check that db is running with the following cmd: 

```bash
curl -k https://<user_name>:<user_passwd>@localhost:${ES_PORT}/"
```

### Init the database (only at first launch):

The database init is launched using a simple shell command. See documentation for needed args.

```bash
TZ=UTC maas_migrate -v --es-ignore-certs-verification True -r ${WORK_DIR}/maas-cds/resources/ --install all &
```

### Engine

#### from local install

The engine is launched using a simple shell command. See documentation for needed args. It will consolidate data on collect events.

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
maas-cds:3.5.1  maas_engine -v --es-ignore-certs-verification True -c "/conf/engine/cds-engine-conf.json"
```

### Collector

The collector is launched using a simple shell command. See documentation for needed args.

#### Collect in local folder

Using reports as files on the local filesystem, the collector will retrieve, report and collect them.

```bash
TZ=UTC python -m maas_collector.rawdata.cli.filesystem -v --es-ignore-certs-verification True -d ${WORK_DIR}/deployment/configuration/collector/ --healthcheck-port ${COLLECTOR_HEALTH_PORT} ${WORK_DIR}/data/reports -p 0 -f
```

#### Collect external services

Using several external api, here odata, the collector will query the service and collect responses.

```bash
TZ=UTC python -m maas_collector.rawdata.cli.odata -v --es-ignore-certs-verification True -d ${WORK_DIR}/deployment/configuration/collector/ --healthcheck-port ${COLLECTOR_HEALTH_PORT} --credential-file ${WORK_DIR}/deployment/configuration/credentials/maas-api-collector-credentials.json -p 0 -f &
```

#### Collect locally using docker image

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
maas-collector:3.5.1 maas_collector.rawdata.cli.filesystem -v --es-ignore-certs-verification True -d ${WORK_DIR}/deployment/configuration/collector/ -f "/data"
```
