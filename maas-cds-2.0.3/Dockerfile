# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.5

ARG DEBIAN_VERSION="bullseye"

#Builder image
FROM python:${PYTHON_VERSION} AS builder

ARG NEXUS_CENTRAL_SERVER="tpzf-central-repository.telespazio.corp:8081"
ARG NEXUS_CENTRAL_USERNAME="maas"
ARG PYPI_REPO_TARGET="maas-pypi-group-develop"
ARG NEXUS_CENTRAL_PASSWORD

WORKDIR /app/

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
  bzip2 \
  sshpass \
  && rm -rf /var/lib/apt/lists/*

# Give PIP env in the command line to ovoid the password to stay in gloval ENV in the containers
RUN PIP_TRUSTED_HOST="${NEXUS_CENTRAL_SERVER}" \
  PIP_INDEX_URL="http://${NEXUS_CENTRAL_USERNAME}:${NEXUS_CENTRAL_PASSWORD}@${NEXUS_CENTRAL_SERVER}/repository/${PYPI_REPO_TARGET}/simple" \
  pip install *.whl
RUN rm -f *.whl

WORKDIR /app

# copy utilities scripts, mainly to use as database initialisation
COPY scripts/ scripts/
#Copy template for opensearch database, as initialisation scripts are provided
COPY resources/ resources/
# Copy default configuration for mass_cds
COPY conf/cds-engine-conf.json conf/default-engine.conf

CMD ["maas_engine", "--config", "/app/conf/default-engine.conf", "--engine-package", "maas_cds"]