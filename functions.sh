#!/usr/bin/env bash

#lib for logs function should be sourced in others script

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

## display status message
function status() {
    if [[ ${1} == 0 ]]; then
        echo
        info "Execution OK"
    else
        echo
        warn "Execution KO"
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

# used for python tox building 
function build_module(){
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
                info "Copy ${MODULE} in dist in folder ${WORK_DIR}/modules/${MODULE}/dist/ ${WORK_DIR}/modules/dist/${MODULE}/."
                cp -ar ${WORK_DIR}/modules/${MODULE}/dist/ ${WORK_DIR}/modules/dist/${MODULE}/
            fi
        else 
            error "${WORK_DIR}/modules/${MODULE}/tox.ini not Found skiping !"
        fi
    fi
}

# used for local module install 
function install_module_localy(){
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
function build_module_docker_image(){
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
            docker build -t "${MODULE}:${DOCKER_TAG_VERSION}" -f "${WORK_DIR}/modules/Dockerfile.${MODULE}" ./modules
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

function omcs_check_venv(){
    if [ -n "${VIRTUAL_ENV}" ] && [ "${VIRTUAL_ENV}" = "${VENV_PATH}" ]; then
        echo "TRUE"
    else
        echo "FALSE"
    fi
}

function omcs_source_venv() {
    if [[ "TRUE" == $(omcs_check_venv) ]] ; then
        info "Python virtual environement ${VENV_NAME} allready sourced!"
    else
        if [ -f "${VENV_PATH}/bin/activate" ]; then
            info "Python virtual environement ${VENV_PATH} exist"
        else
            info "create python virtual environement ${VENV_PATH}"
            python"${PYTHON_VERSION}" -m venv "${VENV_PATH}"
        fi
        info "Sourcing Python virtual environement ${VENV_NAME}"
        source ${VENV_NAME}/bin/activate
    fi
}

function omcs_update_datasources() {
    if [[ "TRUE" == $(omcs_check_venv) ]] ; then
        for DATASOURCE in $(find ${WORK_DIR}/deployment/configuration/grafana/datasources/ -type f -name "*.yaml")
        do
            sed -i "s#@elastic_url@#https://${ES_URL}:${ES_PORT}#g" ${DATASOURCE}
            sed -i "s#@elastic_user@#${ES_USERNAME}#g" ${DATASOURCE}
            sed -i "s#@elastic_user_pwd@#${ES_PASSWORD}#g" ${DATASOURCE}
        done
    else
        warn "Python virtual environement ${VENV_NAME} not sourced! prefer sourcing venv befaure using command \"omcs_source_venv\""
    fi
}

function omcs_cots_start() {
    if [[ "TRUE" == $(omcs_check_venv) ]] ; then
        docker-compose -f ${WORK_DIR}/docker-compose.yaml up -d
    else
        warn "Python virtual environement ${VENV_NAME} not sourced! prefer sourcing venv befaure using command \"omcs_source_venv\""
    fi
}

function omcs_cots_status() {
    if [[ "TRUE" == $(omcs_check_venv) ]] ; then
        docker-compose -f ${WORK_DIR}/docker-compose.yaml ps -d
    else
        warn "Python virtual environement ${VENV_NAME} not sourced! prefer sourcing venv befaure using command \"omcs_source_venv\""
    fi
}

function omcs_cots_stop() {
    if [[ "TRUE" == $(omcs_check_venv) ]] ; then
        docker-compose -f ${WORK_DIR}/docker-compose.yaml down
    else
        echo "Python virtual environement ${VENV_NAME} not sourced! prefer sourcing venv befaure using command \"omcs_source_venv\""
    fi
}

function omcs_cots_clear() {
    if [[ "TRUE" == $(omcs_check_venv) ]] ; then
        docker-compose -f ${WORK_DIR}/docker-compose.yaml stop
        docker-compose -f ${WORK_DIR}/docker-compose.yaml rm
    else
        warn "Python virtual environement ${VENV_NAME} not sourced! prefer sourcing venv befaure using command \"omcs_source_venv\""
    fi
}

function omcs_init_db() {
    if [[ "TRUE" == $(omcs_check_venv) ]] ; then
        TZ=UTC maas_migrate -v --es-ignore-certs-verification True -r ${WORK_DIR}/maas-cds/resources/ --install all | tee ${LOGS_DIR}/init_db.log
    else
        warn "Python virtual environement ${VENV_NAME} not sourced! prefer sourcing venv befaure using command \"omcs_source_venv\""
    fi
}

function omcs_start_engine() {
    if [[ "TRUE" == $(omcs_check_venv) ]] ; then
        TZ=UTC python -m maas_engine -v --es-ignore-certs-verification True -c ${WORK_DIR}/deployment/configuration/engine/cds-engine-conf.json -f --healthcheck-port ${INITDB_HEALTH_PORT} | tee ${LOGS_DIR}/engine.log &
    else
        warn "Python virtual environement ${VENV_NAME} not sourced! prefer sourcing venv befaure using command \"omcs_source_venv\""
    fi
}

function omcs_collect_local_data() {
    if [[ "TRUE" == $(omcs_check_venv) ]] ; then
        TZ=UTC python -m maas_collector.rawdata.cli.filesystem -v --es-ignore-certs-verification True -d ${WORK_DIR}/deployment/configuration/collector/ --healthcheck-port ${COLLECTOR_HEALTH_PORT} ${WORK_DIR}/data/reports -p 0 -f | tee ${LOGS_DIR}/collecte_local.log
    else
        warn "Python virtual environement ${VENV_NAME} not sourced! prefer sourcing venv befaure using command \"omcs_source_venv\""
    fi
}

function omcs_collect_external_data() {
    if [[ "TRUE" == $(omcs_check_venv) ]] ; then
        TZ=UTC python -m maas_collector.rawdata.cli.odata -v --es-ignore-certs-verification True -d ${WORK_DIR}/deployment/configuration/collector/ --healthcheck-port ${COLLECTOR_HEALTH_PORT} --credential-file ${WORK_DIR}/deployment/configuration/credentials/maas-api-collector-credentials.json -p 0 -f | tee ${LOGS_DIR}/collecte_external.log
    else
        warn "Python virtual environement ${VENV_NAME} not sourced! prefer sourcing venv befaure using command \"omcs_source_venv\""
    fi
}


function omcs_help() {
    echo "Launch local build  : ./local_build.sh"
    echo "Launch dockers build: ./dockers_build.sh"
}