# Omcs Installation and running

Omcs is a complete solution for monitoring process, it's based on microservices to collect, compute and display monitoring informations.
It use severals components:

- Elasticsearch (Opendistro) for data storage.
- Grafana for data display.
- RabbitMq for communication between components.
- MAAS-Collector for data collecte.
- MAAS-CDS ( based on MAAS-Engine) for data compute

It depends on Python:

- Python 3.11 as MAAS-XXXX is coded in python

## Install

### Get the sources

Sources are disponible on [GitHub](https://github.com/coordinationdesk/end2end_monitoring_dashboard).

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

Update,correct and source your environement.

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

All cots are used as docker containers and could be organized  in a docker-compose file:

```bash
cat ${WORK_DIR}/docker-compose.yaml
```

To launch cots uses `docker-compose`commands:

```bash
docker-compose -f ${WORK_DIR}/docker-compose.yaml up -d
```

### Build maas components

Maas components are python modules, they should be build and install using pip.

First python 3.11, pip should be installed on the destination server.

Define a vitual env for the maas comopnents.

```bash
python${PYTHON_VERSION} -m venv ${WORK_DIR}/omcs-venv-${PYTHON_VERSION}
source ${WORK_DIR}/omcs-venv-${PYTHON_VERSION}/bin/activate
```

Install maas components python modules using pip.

```bash
pip install -e ${WORK_DIR}/maas-model/
pip install -e ${WORK_DIR}/maas-engine/
pip install -e ${WORK_DIR}/maas-collector/
pip install -e ${WORK_DIR}/maas-cds/
```

To build wheel uses tox command:

```bash
tox -c ${WORK_DIR}/maas-model/tox.ini -e build
tox -c ${WORK_DIR}/maas-engine/tox.ini -e build
tox -c ${WORK_DIR}/maas-collector/tox.ini -e build
tox -c ${WORK_DIR}/maas-cds/tox.ini -e build
```

To build docker images uses docker build commands.
To get git tag version uses git command:

```bash
COLLECTOR_TAG_VERSION=$(git --git-dir=${WORK_DIR}/modules/maas-collector/.git describe --tags --exact-match)
docker build -t "maas-collector:${COLLECTOR_TAG_VERSION}" -f "${WORK_DIR}/modules/Dockerfile.maas-collector" ./modules
CDS_TAG_VERSION=$(git --git-dir=${WORK_DIR}/modules/maas-collector/.git describe --tags --exact-match)
docker build -t "maas-cds:${CDS_TAG_VERSION}" -f "${WORK_DIR}/modules/Dockerfile.maas-cds" ./modules
```

## Configure MAAS

Some configuration should be set for MAAS usage:

### Grafana

Dashboards and datasources should be set for grafana.

They are delivered in the github.

You could find them in folder:

```bash
ls -al ${WORK_DIR}/configuration/grafana
```

### MAAS-engine

The maas engine need configuration this omcs specific configuration.

They are delivered in the github.

You clould find them in folder:

```bash
ls -al ${WORK_DIR}/configuration/engines/cds-engine-conf.json
```

### MAAS-collector

The maas engine need configuration this omcs specific configuration.

They are delivered in the github.

You clould find them in folder:

```bash
ls -al ${WORK_DIR}/configuration/collector/
```

### Credentials

The maas collector need to collect externals interfaces credenTials file.

They are not deliverded in github a sample file is delivered, corrects values should be set in file:

```bash
ls -al ${WORK_DIR}/configuration/credentials/maas-api-collector-credentials.json
```

## Launch MAAS

### Cots

To start the application cots use docker-compose command:

```bash
docker-compose -f ${WORK_DIR}/docker-compose.yaml up -d
```

Service could be found here:

- [elasticsearch](https://localhost:9200) (admin:admin)
- [rabbitmq](http://localhost:15672) (guest:guest)
- [grafana](http://localhost:3000)

### Init the database (only at first launch):

The database init is launched using a simple shell command see documentation for needed args.

```bash
TZ=UTC maas_migrate -v --es-ignore-certs-verification True -r ${WORK_DIR}/maas-cds/resources/ --install all &
```

### Engine

The engine is launched using a simple shell command see documentation for needed args it will consolidate datas on collecte events.

```bash
TZ=UTC python -m maas_engine -v --es-ignore-certs-verification True -c ${WORK_DIR}/configuration/engines/cds-engine-conf.json -f --healthcheck-port ${ENGINE_HEALTH_PORT}
```

### Collector

The collector is launched using a simple shell command see documentation for needed args.

#### Collect in local folder

Using reports as file on local filesystem the collector will retrieve reports and collect them.

```bash
TZ=UTC python -m maas_collector.rawdata.cli.filesystem -v --es-ignore-certs-verification True -d ${WORK_DIR}/configuration/collector/ --healthcheck-port ${COLLECTOR_HEALTH_PORT} ${WORK_DIR}/data/reports -p 0 -f
```

#### Collect external services

Using severals external api here odata the collector will query the service and collect responces.

```bash
TZ=UTC python -m maas_collector.rawdata.cli.odata -v --es-ignore-certs-verification True -d ${WORK_DIR}/configuration/collector/ --healthcheck-port ${COLLECTOR_HEALTH_PORT} --credential-file ${WORK_DIR}/configuration/credentials/maas-api-collector-credentials.json -p 0 -f &
```
