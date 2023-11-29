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
