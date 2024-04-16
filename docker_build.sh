#! /bin/bash

source "./functions.sh"

if [ -z "${omcs_ENV_SETTED}" ]; then
    source env.sh
    info "env sourced"
else
    info "env sourced"
fi

if [ -f "${VENV_PATH}/bin/activate" ]; then
    info "Python virtual environement ${VENV_PATH} exist"
else
    info "create python virtual environement ${VENV_PATH}"
    python"${PYTHON_VERSION}" -m venv "${VENV_PATH}"
fi

if [ -n "${VIRTUAL_ENV}" ] && [ "${VIRTUAL_ENV}" = "${VENV_PATH}" ]; then
    echo "Python virtual environement ${VENV_PATH} sourced!"
else
    source "${VENV_PATH}/bin/activate"
fi

build_module maas-model
build_module maas-engine
build_module maas-collector
build_module maas-cds
build_module_docker_image maas-collector ${COLLECTOR_TAG_VERSION}
build_module_docker_image maas-cds ${CDS_TAG_VERSION}

echo ""
echo ""
echo ""
echo ""
echo ""
echo "############"
echo "#   HELP   #"
echo "############"
echo ""
echo " Run builded dockers:"
echo " - launch cots cmd : docker-compose -f ${WORK_DIR}/docker-compose.yaml up -d"
echo " - wait for dockers to be up an ready check cmd : omcs_cots_status"
echo " - check db is running cmd : curl -k https://$\{ES_USERNAME}:$\{ES_PASSWORD}@localhost:$\{ES_PORT}/"
echo " - init db:"
echo ""
echo " docker run -it --rm -v \"${WORK_DIR}/configuration/:/conf\" -e \"ES_USERNAME=$\{ES_USERNAME}\" -e \"ES_PASSWORD=$\{ES_PASSWORD}\" -e \"ES_PORT=$\{ES_PORT}\" -e \"ES_URL=$\{ES_URL}\" -e \"AMQP_PORT=$\{AMQP_PORT}\" -e \"AMQP_IHM_PORT=$\{AMQP_IHM_PORT}\" -e \"AMQP_URL=$\{AMQP_URL}\" -e \"AMQP_USERNAME=$\{AMQP_USERNAME}\" -e \"AMQP_PASSWORD=$\{AMQP_PASSWORD}\" --network host maas-cds:${CDS_TAG_VERSION} maas_migrate -v --es-ignore-certs-verification True -r \"${WORK_DIR}/maas-cds/resources/\" --install all --populate cds-s2-tilpar-tiles.bulk.xz"
echo ""
echo " - launch engine docker cmd :"
echo ""
echo " docker run -it --rm -v \"$PWD/configuration/:/conf\" -e \"ES_USERNAME=$\{ES_USERNAME}\" -e \"ES_PASSWORD=$\{ES_PASSWORD}\" -e \"ES_PORT=$\{ES_PORT}\" -e \"ES_URL=$\{ES_URL}\" -e \"AMQP_PORT=$\{AMQP_PORT}\" -e \"AMQP_IHM_PORT=$\{AMQP_IHM_PORT}\" -e \"AMQP_URL=$\{AMQP_URL}\" -e \"AMQP_USERNAME=$\{AMQP_USERNAME}\" -e \"AMQP_PASSWORD=$\{AMQP_PASSWORD}\" --network host maas-cds:${CDS_TAG_VERSION}  maas_engine -v --es-ignore-certs-verification True -c \"/conf/engine/cds-engine-conf.json\""
echo "  "
echo "  "
echo " - launch engine docker cmd :"
echo "  "
echo " docker run -it --rm -v \"$\{PWD}/data/:/data\" -v \"$\{PWD}/configuration/:/conf\" -e \"ES_USERNAME=$\{ES_USERNAME}\" -e \"ES_PASSWORD=$\{ES_PASSWORD}\" -e \"ES_PORT=$\{ES_PORT}\" -e \"ES_URL=$\{ES_URL}\" -e \"AMQP_PORT=$\{AMQP_PORT}\" -e \"AMQP_IHM_PORT=$\{AMQP_IHM_PORT}\" -e \"AMQP_URL=$\{AMQP_URL}\" -e \"AMQP_USERNAME=$\{AMQP_USERNAME}\" -e \"AMQP_PASSWORD=$\{AMQP_PASSWORD}\" --network host maas-collector:${COLLECTOR_TAG_VERSION} maas_collector.rawdata.cli.filesystem -v --es-ignore-certs-verification True -c \"/conf/engine/cds-engine-conf.json\" -f \"/data\""