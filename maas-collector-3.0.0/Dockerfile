# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.5

ARG DEBIAN_VERSION="bullseye"

#Builder image
FROM python:${PYTHON_VERSION} AS builder

ARG NEXUS_CENTRAL_SERVER="tpzf-central-repository.telespazio.corp:8081"
ARG NEXUS_CENTRAL_USERNAME="maas"
ARG PYPI_REPO_TARGET="maas-pypi-group-develop"
ARG NEXUS_CENTRAL_PASSWORD

WORKDIR /app

COPY . .

# PIP env must be given globaly, otherwise 'build' module don't see them !! bad module!!
ENV PIP_TRUSTED_HOST="${NEXUS_CENTRAL_SERVER}"
ENV PIP_INDEX="http://${NEXUS_CENTRAL_SERVER}/repository/${PYPI_REPO_TARGET}/"
ENV PIP_INDEX_URL="http://${NEXUS_CENTRAL_USERNAME}:${NEXUS_CENTRAL_PASSWORD}@${NEXUS_CENTRAL_SERVER}/repository/${PYPI_REPO_TARGET}/simple"

RUN rm -rf dist/* \
  && pip install . build \
  && python -m build


#Final image
FROM python:${PYTHON_VERSION}-slim-${DEBIAN_VERSION}
LABEL Author="TELESPAZIO FRANCE"

ARG NEXUS_CENTRAL_SERVER="tpzf-central-repository.telespazio.corp:8081"
ARG NEXUS_CENTRAL_USERNAME="maas"
ARG PYPI_REPO_TARGET="maas-pypi-group-develop"
ARG NEXUS_CENTRAL_PASSWORD

WORKDIR /tmp

COPY --from=builder /app/dist/*.whl ./

# update distrib and add needed tools
# follow best pratices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#sort-multi-line-arguments
RUN apt-get update && apt-get install -y \
  curl \
  jq \
  && rm -rf /var/lib/apt/lists/*

RUN PIP_TRUSTED_HOST="${NEXUS_CENTRAL_SERVER}" \
  PIP_INDEX_URL="http://${NEXUS_CENTRAL_USERNAME}:${NEXUS_CENTRAL_PASSWORD}@${NEXUS_CENTRAL_SERVER}/repository/${PYPI_REPO_TARGET}/simple" \
  pip install *.whl
RUN rm -f *.whl

WORKDIR /app

# copy utilities scripts, mainly to use as database initialisation
COPY scripts/ scripts/

VOLUME ["/conf", "/data"]

ENTRYPOINT [ "python", "-m"]
CMD [ "maas_collector.rawdata.cli.filesystem", "-v", "/data" ]

#Elsatic url : http://admin:admin@monitoring.stage.maas.telespazio.corp:80/opensearch or http://admin:admin@localhost:9200
# RabbitMQ url : http://guest:guest@localhost:5672 or ????

## launch as a filesytem consumer
# docker run -it --rm \
#   -v $PWD/tests/data/:/data \
#   -v $PWD/tests/conf:/conf \
#   -e "ES_URL=http://admin:admin@localhost:9200" \
#   -e "AMQP_URL=http://guest:guest@localhost:5672" \
#   maas-collector

## launch as a S3 bucket listener
# docker run -it --rm \
#   -v $PWD/tests/conf:/conf \
#   -e "ES_URL=http://admin:admin@localhost:9200" \
#   -e "AMQP_URL=http://guest:guest@localhost:5672" \
#   -e "S3_ENDPOINT=http://s3.maas.telespazio.corp" \
#   -e "S3_KEY_ID=maasminio" \
#   -e "S3_ACCESS_KEY=maasminio" \
#   -e "S3_BUCKET=rawdata" \
#   maas-collector maas_collector.rawdata.cli.s3