#!/usr/bin/env bash

#set -x

##############################################################
#
# omcs specfics env variable to be updated accordingly to your needs
#

# build env variables
export omcs_ENV_SETTED="True"
export PYTHON_VERSION="3.11"
export WORK_DIR=$(readlink -f ".")
export LOGS_DIR="${WORK_DIR}/logs"
export LOG_FILE="${LOGS_DIR}/omcs_script.logs"
export VENV_NAME=omcs-venv
export VENV_PATH=${WORK_DIR}/${VENV_NAME}
export CDS_TAG_VERSION=2.4.1
export COLLECTOR_TAG_VERSION=3.5.1

# execution env variables
export ES_USERNAME=admin
export ES_PASSWORD=StrongP4sSword!!or-N-o-t
export ES_PORT=9200
export ES_URL=https://localhost:${ES_PORT}/
export AMQP_PORT=5672
export AMQP_IHM_PORT=15672
export AMQP_URL=amqp://localhost:${AMQP_PORT}//
export AMQP_USERNAME=guest
export AMQP_PASSWORD=guest
export GRF_PORT=3000
export HEALTHCHECK_HOSTNAME=0.0.0.0
export INITDB_HEALTH_PORT=49250
export ENGINE_HEALTH_PORT=49251
export COLLECTOR_HEALTH_PORT=49252

#
# omcs specfics env variable to be updated accordingly to your needs
#
##############################################################


if [ -z "${VERBOSE}" ]; then
    VERBOSE="true"
fi
if [ -z "${ASK}" ]; then
    ASK="true"
fi
if [ -z "${DEBUG}" ]; then
    DEBUG="false"
fi
if [ -z "${LOG_IN_FILE}" ]; then
    LOG_IN_FILE="false"
fi
if [ -z "${NO_EXECUTE}" ]; then
    NO_EXECUTE="false"
fi
if [ -z "${LOG_FILE}" ]; then
    LOG_FILE="${SCRIPT_NAME}.log"
fi
if [[ -t 2 ]] && [[ -z "${NO_COLOR-}" ]] && [[ "${TERM-}" != "dumb" ]]; then
    NOFORMAT='\033[0m'
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    BGREEN='\033[1;32m' 
    ORANGE='\033[0;33m'
    BLUE='\033[0;34m'
    PURPLE='\033[0;35m'
    CYAN='\033[0;36m'
    YELLOW='\033[1;33m'
else
    NOFORMAT=''
    RED=''
    GREEN=''
    ORANGE=''
    BLUE=''
    PURPLE=''
    CYAN=''
    YELLOW=''
fi

## display a message
function msg() {
    if [[ ${VERBOSE} == "true" ]]; then
        echo >&2 -e "[${BLUE}MSG  ${NOFORMAT}] "${1-}
    fi
    if [[ ${LOG_IN_FILE} == "true" ]]; then
        echo >&2 -e "$(/bin/date "+%Y-%m-%dT%H:%M:%S") [MSG ] "${1-} >>${LOG_FILE}
    fi
}

## display info message
function info() {
    if [[ ${VERBOSE} == "true" ]]; then
        echo >&2 -e "[${GREEN}INFO ${NOFORMAT}] "${1-}
    fi
    if [[ ${LOG_IN_FILE} == "true" ]]; then
        echo >&2 -e "$(/bin/date "+%Y-%m-%dT%H:%M:%S") [INFO ] "${1-} >>${LOG_FILE}
    fi
}

## display info message
function ack() {
    if [[ ${VERBOSE} == "true" ]]; then
        echo >&2 -e "[${BGREEN} OK  ${NOFORMAT}] "${1-}
    fi
    if [[ ${LOG_IN_FILE} == "true" ]]; then
        echo >&2 -e "$(/bin/date "+%Y-%m-%dT%H:%M:%S") [ OK  ] "${1-} >>${LOG_FILE}
    fi
}

## display warning message
function warn() {
    if [[ ${VERBOSE} == "true" ]]; then
        echo >&2 -e "[${YELLOW}WARN ${NOFORMAT}] "${1-}
    fi
    if [[ ${LOG_IN_FILE} == "true" ]]; then
        echo >&2 -e "$(/bin/date "+%Y-%m-%dT%H:%M:%S") [WARN ] "${1-} >>${LOG_FILE}
    fi
}

## display error message
function error() {
    if [[ ${VERBOSE} == "true" ]]; then
        echo >&2 -e "[${RED}ERROR${NOFORMAT}] "${1-}
    fi
    if [[ ${LOG_IN_FILE} == "true" ]]; then
        echo >&2 -e "$(/bin/date "+%Y-%m-%dT%H:%M:%S") [ERROR] "${1-} >>${LOG_FILE}
    fi
}

## display critical message
function criti() {
    if [[ ${VERBOSE} == "true" ]]; then
        echo >&2 -e "[${RED}CRITI${NOFORMAT}] "${1-}
    fi
    if [[ ${LOG_IN_FILE} == "true" ]]; then
        echo >&2 -e "$(/bin/date "+%Y-%m-%dT%H:%M:%S") [CRITI] "${1-} >>${LOG_FILE}
    fi
}

## display debug message
function debug() {
    if [[ ${DEBUG} == "true" ]]; then
        echo >&2 -e "[${BLUE}DEBUG${NOFORMAT}] "${1-}
        if [[ ${LOG_IN_FILE} == "true" ]]; then
            echo >&2 -e "$(/bin/date "+%Y-%m-%dT%H:%M:%S") [DEBUG] "${1-} >>${LOG_FILE}
        fi
    fi
}

## ask for command message
function ask() {
    if [ $# -lt 2 ]; then
        error "Unable to perform ask command bad args number given args :\"${*}\""
    else
        local _QUESTION=${1}
        shift 1
        local _COMMAND=${*}
        if [[ ${ASK} == "true" ]]; then
            echo >&2 -en "[${BLUE}ASK${NOFORMAT}  ] ${_QUESTION}"
            read -r -p " [N/y] " response
            case "${response}" in
            y)
                ${_COMMAND}
                ;;
            c)
                ASK="false"
                ${_COMMAND}
                ;;
            *)
                warn "Skip :  ${_QUESTION} [${_COMMAND}]"
                ;;
            esac
        else
            msg "${_QUESTION}"
            ${_COMMAND}
        fi
    fi
}

function omcs_env_display(){
    msg "Build env variables"
    msg "omcs_ENV_SETTED=${omcs_ENV_SETTED}"
    msg "PYTHON_VERSION=${PYTHON_VERSION}"
    msg "WORK_DIR=${WORK_DIR}"
    msg "LOGS_DIR=${LOGS_DIR}"
    msg "LOG_FILE=${LOG_FILE}"
    msg "VENV_NAME=${VENV_NAME}"
    msg "VENV_PATH=${VENV_PATH}"
    msg CDS_TAG_VERSION=${CDS_TAG_VERSION}
    msg COLLECTOR_TAG_VERSION=${COLLECTOR_TAG_VERSION}
    msg "Execution env variables"
    msg "ES_USERNAME=${ES_USERNAME}"
    msg "ES_PASSWORD=XXXXXX"
    msg "ES_PORT=${ES_PORT}"
    msg "ES_URL=${ES_URL}"
    msg "AMQP_PORT=${AMQP_PORT}"
    msg "AMQP_IHM_PORT=${AMQP_IHM_PORT}"
    msg "AMQP_URL=${AMQP_URL}"
    msg "AMQP_USERNAME=${AMQP_USERNAME}"
    msg "AMQP_PASSWORD=XXXXXX"
    msg "GRF_PORT=${GRF_PORT}"
    msg "HEALTHCHECK_HOSTNAME=${HEALTHCHECK_HOSTNAME}"
    msg "INITDB_HEALTH_PORT=${INITDB_HEALTH_PORT}"
    msg "ENGINE_HEALTH_PORT=${ENGINE_HEALTH_PORT}"
    msg "COLLECTOR_HEALTH_PORT=${COLLECTOR_HEALTH_PORT}"
}

function omcs_venv_check(){
    echo "VIRTUAL_ENV=${VIRTUAL_ENV} VENV_PATH=${VENV_PATH}"
    if [ -d ${VENV_PATH} ]; then
        if [ -n "${VIRTUAL_ENV}" ];then
            if [ "${VIRTUAL_ENV}" = "${VENV_PATH}" ]; then
        echo "TRUE"
    else
                warn "sourced venv: ${VIRTUAL_ENV} is not ${VENV_NAME} venv!"
                exit
            fi
        else
            warn "No virtual environement sourced !" 
            exit
        fi
    else
        warn "No ${VENV_NAME} created! ${VENV_PATH} does not exist !" 
        exit
    fi
}

function omcs_venv_create() {
    info "create python virtual environement ${VENV_PATH}"
    python"${PYTHON_VERSION}" -m venv "${VENV_PATH}"
}

function omcs_venv_source() {
    if [[ "TRUE" == $(omcs_venv_check) ]] ; then
        info "Python virtual environement ${VENV_NAME} allready sourced!"
    else
        if [ -f "${VENV_PATH}/bin/activate" ]; then
            info "Python virtual environement ${VENV_PATH} exist"
        else
            omcs_venv_create
        fi
        info "Sourcing Python virtual environement ${VENV_NAME}"
        source ${VENV_PATH}/bin/activate
    fi
}

function omcs_update_datasources() {
    omcs_venv_source
    for DATASOURCE in $(find ${WORK_DIR}/deployment/configuration/grafana/datasources/ -type f -name "*.yaml")
    do
        sed -i "s#@elastic_url@#https://${ES_URL}:${ES_PORT}#g" ${DATASOURCE}
        sed -i "s#@elastic_user@#${ES_USERNAME}#g" ${DATASOURCE}
        sed -i "s#@elastic_user_pwd@#${ES_PASSWORD}#g" ${DATASOURCE}
    done
}

function omcs_cots_start() {
    omcs_venv_source
    docker-compose -f ${WORK_DIR}/cots/docker-compose.yaml up -d
}

function omcs_cots_status() {
    omcs_venv_source
    docker-compose -f ${WORK_DIR}/cots/docker-compose.yaml ps -d
}

function omcs_cots_stop() {
    omcs_venv_source
    docker-compose -f ${WORK_DIR}/cots/docker-compose.yaml down
}

function omcs_cots_clear() {
    omcs_venv_source
    docker-compose -f ${WORK_DIR}/cots/docker-compose.yaml stop
    docker-compose -f ${WORK_DIR}/cots/docker-compose.yaml rm
}

function omcs_init_db() {
    omcs_venv_source
    TZ=UTC maas_migrate -v --es-ignore-certs-verification True -r ${WORK_DIR}/maas-cds/resources/ --install all | tee ${LOGS_DIR}/init_db.log
}

function omcs_start_engine() {
    omcs_venv_source
    TZ=UTC python -m maas_engine -v --es-ignore-certs-verification True -c ${WORK_DIR}/deployment/configuration/engine/cds-engine-conf.json -f --healthcheck-port ${INITDB_HEALTH_PORT} | tee ${LOGS_DIR}/engine.log &
}

function omcs_collect_local_data() {
    omcs_venv_source
    TZ=UTC python -m maas_collector.rawdata.cli.filesystem -v --es-ignore-certs-verification True -d ${WORK_DIR}/deployment/configuration/collector/ --healthcheck-port ${COLLECTOR_HEALTH_PORT} ${WORK_DIR}/data/reports -p 0 -f | tee ${LOGS_DIR}/collecte_local.log
}

function omcs_collect_external_data() {
    omcs_venv_source
    TZ=UTC python -m maas_collector.rawdata.cli.odata -v --es-ignore-certs-verification True -d ${WORK_DIR}/deployment/configuration/collector/ --healthcheck-port ${COLLECTOR_HEALTH_PORT} --credential-file ${WORK_DIR}/deployment/configuration/credentials/maas-api-collector-credentials.json -p 0 -f | tee ${LOGS_DIR}/collecte_external.log
}

# used for python tox building 
function omcs_python_module_build(){
    if [ -z "${1}" ] ; then
        error "No module to build given!"
    else
        MODULE="${1}"
        msg "Build ${MODULE}"
        if [ -f "${WORK_DIR}/modules/${MODULE}/tox.ini" ]; then
            info "${MODULE} found."
            tox -c ${WORK_DIR}/modules/${MODULE}/tox.ini -e build
            retVal=$?
            if [ $retVal -ne 0 ]; then
                error "Building ${MODULE}"
            else
                info "Build ${MODULE} done"
                info "Copy ${MODULE} in folder ${WORK_DIR}/modules/build/${MODULE}/ ."
                mkdir -p ${WORK_DIR}/modules/build/${MODULE}/
                cp -ar ${WORK_DIR}/modules/${MODULE}/dist/ ${WORK_DIR}/modules/build/${MODULE}/
            fi
        else 
            error "${WORK_DIR}/modules/${MODULE}/tox.ini not Found skiping !"
        fi
    fi
}

# used for local module install 
function omcs_python_module_install_localy(){
    if [ -z "${1}" ] ; then
        error "No module to install given!"
    else
        MODULE="${1}"
        msg "Install ${MODULE}"
        if [ $(find ./modules/maas-collector/dist -name "*.whl" | wc -l) ]; then
            info "${MODULE} weel found."
            pip install ${WORK_DIR}/modules/${MODULE}/dist/*.whl
            retVal=$?
            if [ $retVal -ne 0 ]; then
                error "Installing ${MODULE}"
            else
                info "Install ${MODULE} done"
            fi
        else 
            error "${WORK_DIR}/modules/${MODULE}/dist/*.whl not Found skiping !"
        fi
    fi
}

# used for docker image building 
function omcs_docker_build(){
    if [ -z "${1}" ] ; then
        error "No module to docker image build given!"
    else
        MODULE="${1}"
        if [ -z "${2}" ] ; then
            DOCKER_TAG_VERSION=${2}
        else
            DOCKER_TAG_VERSION=${2}
        fi
        msg "Build Docker Image for ${MODULE}:${DOCKER_TAG_VERSION}"
        if [ -f "${WORK_DIR}/modules/Dockerfile.${MODULE}" ]; then
            info "${MODULE} found."
            docker build -t "${MODULE}:${DOCKER_TAG_VERSION}" -f "${WORK_DIR}/modules/Dockerfile.${MODULE}" ${WORK_DIR}/modules
            retVal=$?
            if [ $retVal -ne 0 ]; then
                error "Building Docker Image for ${MODULE}"
            else
                info "Build Docker Image for ${MODULE} done"
            fi
        else 
            error "${WORK_DIR}/modules/Dockerfile.${MODULE} not Found skiping !"
        fi
    fi
}

# used for local install
function omcs_python_modules_install_localy(){
    omcs_venv_source
    omcs_python_module_build maas-model
    omcs_python_module_build maas-engine
    omcs_python_module_build maas-collector
    omcs_python_module_build maas-cds
    omcs_python_module_install_localy maas-model
    omcs_python_module_install_localy maas-engine
    omcs_python_module_install_localy maas-collector
    omcs_python_module_install_localy maas-cds
}

# used to build all python modules
function omcs_python_modules_build(){
    omcs_venv_source
    omcs_python_module_build maas-model
    omcs_python_module_build maas-engine
    omcs_python_module_build maas-collector
    omcs_python_module_build maas-cds
}

# used to build all dockers
function omcs_dockers_build(){
    omcs_venv_source
    omcs_docker_build maas-collector ${COLLECTOR_TAG_VERSION}
    omcs_docker_build maas-cds ${CDS_TAG_VERSION}
}

# used to save all docker images as files
function omcs_docker_image_save(){
    msg "Write maas-collector:${COLLECTOR_TAG_VERSION} docker image in ${WORK_DIR}/modules/build/maas-collector/maas-collector_${COLLECTOR_TAG_VERSION}.docker.tar.gz"
    docker image save maas-collector:${COLLECTOR_TAG_VERSION} -o ${WORK_DIR}/modules/build/maas-collector/maas-collector_${COLLECTOR_TAG_VERSION}.docker.tar
    gzip ${WORK_DIR}/modules/build/maas-collector/maas-collector_${COLLECTOR_TAG_VERSION}.docker.tar
    msg "Write maas-cds/maas-cds_${CDS_TAG_VERSION} docker image in ${WORK_DIR}/modules/build/maas-collector/maas-cds/maas-cds_${CDS_TAG_VERSION}.docker.tar.gz"
    docker image save maas-cds:${CDS_TAG_VERSION} -o ${WORK_DIR}/modules/build/maas-cds/maas-cds_${CDS_TAG_VERSION}.docker.tar
    gzip ${WORK_DIR}/modules/build/maas-cds/maas-cds_${CDS_TAG_VERSION}.docker.tar
}

omcs_env_display
