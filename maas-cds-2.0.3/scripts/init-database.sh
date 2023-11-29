#!/bin/bash
#set -x

# get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
RESOURCE_DIR="${PARENT_DIR}/resources"
TEMPLATE_DIR="${RESOURCE_DIR}/templates"
#source lib functions
. ${SCRIPT_DIR}/lib/functions.sh

# init default values
DATA_PERIOD="from_template"
INDICES=""

TRUST="false"

TMP_JSON_OUT=".tmp.out.json"

## display usage help message
function usage() {
    echo "$0"
    echo "  init options:"
    echo "   -e set full opensearch url (default http://localhost:9200)"
    echo "   -u set opensearch user (default admin)"
    echo "   -p set opensearch password (default XXXXXXXXX)"
    echo "   -d set the data period used to push one in from_template,day,month,year,all, a setted suffix ex \"-2022-04#"
    echo "   -i set the indexes to import a double coted list of index names (default \"${INDICES}\")"
    echo "   -t trust do not inspect es return"
    echo "   -c clean part files"
    echo ""
    echo "samples :"
    echo ""
    echo "   Init es datastrip and downlink for the year 2021, es is on http://localhost:9200 with default auth"
    echo "     $0"
    echo ""
    echo "   Init es datastrip for the 2021/04/29 day, es is on https://127.0.0.1:8081"
    echo "     $0 -e https://127.0.0.1:8081 -d day -i produced_datastrip"
    echo ""
    echo "   Init es datastrip and downlink for the year 2021, es is on https://127.0.0.1:8081 with user toto and pwd titi"
    echo "     $0 -e https://127.0.0.1:8081 -u toto -p titi"
}

# set options
while getopts "he:u:p:d:i:tnc" opt; do
    case $opt in
    h)
        usage
        exit 1
        ;;
    e)
        ES_URL="${OPTARG}"
        ;;
    u)
        ES_USER="${OPTARG}"
        ;;
    p)
        ES_PWD="${OPTARG}"
        ;;
    d)
        DATA_PERIOD="${OPTARG}"
        ;;
    i)
        INDICES="${OPTARG}"
        ;;
    c)
        CLEAN="true"
        ;;
    n)
        NO_EXECUTE="-n"
        ;;
    t)
        TRUST="true"
        ;;
    \?)
        warn "Invalid option: -${OPTARG}" >&2
        usage
        exit
        ;;
    esac
done

# init es url
if [[ -z ${ES_URL} ]]; then
    ES_URL="http://localhost:9200"
fi
# init es user
if [[ -z ${ES_USER} ]]; then
    ES_USER="admin"
fi
# init es pwd
if [[ -z ${ES_PWD} ]]; then
    ES_PWD="admin" #
fi

function call_es_wrapper() {
    local DOMAIN=${1}
    local ACTION=${2}
    local INDICE=${3}
    local OPTIONS=${4}

    if [[ "${TRUST}" = "false" ]]; then
        local RESULT_FILE="${DOMAIN}_${ACTION}_${INDICE}_$(date '+%s')${TMP_JSON_OUT}"
    else
        #local RESULT_FILE="/dev/null"
        local RESULT_FILE="${DOMAIN}_${ACTION}_${INDICE}_$(date '+%s')${TMP_JSON_OUT}"
    fi
    msg "Perform ${ACTION} ${DOMAIN} ${INDICE}"
    ${SCRIPT_DIR}/lib/es_wrapper.sh -v -D ${DOMAIN} -A ${ACTION} -I ${INDICE} -p ${OPTIONS} -e "${ES_URL}" -a "${ES_USER}:${ES_PWD}" ${NO_EXECUTE} >${RESULT_FILE}

    if [[ "${TRUST}" = "false" ]]; then
        if [[ "${ACTION}" == "DELETE" ]]; then
            OUT=$(jq -r '.acknowledged' "${RESULT_FILE}")
            if [[ "${OUT}" == "true" ]]; then
                ack "${INDICE} ${ACTION} OK"
                rm ${RESULT_FILE}
            else
                OUT=$(jq -r '.error.root_cause[0].type' "${RESULT_FILE}")
                if [[ "${OUT}" == "index_template_missing_exception" || "${OUT}" == "index_not_found_exception" ]]; then
                    warn "${INDICE} ${ACTION} WARN : ${OUT}"
                    rm ${RESULT_FILE}
                else
                    debug "${SCRIPT_DIR}/lib/es_wrapper.sh -v -D ${DOMAIN} -A ${ACTION} -I ${INDICE} -p ${OPTIONS} -e \"${ES_URL}\" -a \"${ES_USER}:${ES_PWD}\" ${NO_EXECUTE}"
                    error "${INDICE} ${ACTION} ERROR : see ${RESULT_FILE}"
                fi
            fi
        else
            OUT=$(jq -r '.acknowledged' "${RESULT_FILE}")
            if [[ "${OUT}" == "true" ]]; then
                ack "${INDICE} ${ACTION}"
                rm ${RESULT_FILE}
            else
                OUT=$(jq -r '.errors' "${RESULT_FILE}")
                if [[ "${OUT}" == "false" ]]; then
                    ack "${INDICE} ${ACTION}"
                    rm ${RESULT_FILE}
                else
                    debug "${SCRIPT_DIR}/lib/es_wrapper.sh -v -D ${DOMAIN} -A ${ACTION} -I ${INDICE} -p ${OPTIONS} -e \"${ES_URL}\" -a \"${ES_USER}:${ES_PWD}\" ${NO_EXECUTE}"
                    error "${INDICE} ${ACTION} ERROR : see ${RESULT_FILE}"
                fi
            fi
        fi
    fi
}

function update_index() {
    local INDEX=$1
    local SUFFIX=$2
    msg "= ${INDEX} ============"
    call_es_wrapper "TEMPLATE" "DELETE" "template_${INDEX}"
    call_es_wrapper "INDEX" "DELETE" "${INDEX}${SUFFIX}"
    if [[ "${CLEAN}" != "true" ]]; then
        call_es_wrapper "TEMPLATE" "POPULATE" "template_${INDEX}" "-d ${TEMPLATE_DIR}/${INDEX}_template.json"
        call_es_wrapper "INDEX" "INIT" "${INDEX}${SUFFIX}"
    fi
}

function get_suffix_from_template() {
    local INDEX=${1}
    SUFFIX=""
    SUFFIX_FORMAT="-$(cat ${TEMPLATE_DIR}/${INDEX}_template.json | jq -r '.mappings._meta.partition_format')"
    if [[ "${SUFFIX_FORMAT}" == "-%Y-%m-%d" ]]; then
        SUFFIX="-$(date +%Y-%m-%d)"
    elif [[ "${SUFFIX_FORMAT}" == "-%Y-%m" ]]; then
        SUFFIX="-$(date +%Y-%m)"
    elif [[ "${SUFFIX_FORMAT}" == "-%Y" ]]; then
        SUFFIX="-$(date +%Y)"
    else
        SUFFIX="${SUFFIX_FORMAT}"
    fi
}

msg "==== START  ====="

if [[ "${TMP_JSON_OUT}" != "" ]]; then
    rm --preserve-root=all -f *${TMP_JSON_OUT}
fi

# scan template folder if no indeices provided
if [ -z "${INDICES}" ]; then
    msg "Scan template folder to fond templates:"
    for TEMPLATE_FILE in $(ls ${TEMPLATE_DIR}/*_template.json); do
        TEMPLATE_FILE=${TEMPLATE_FILE##*/}
        INDEX=${TEMPLATE_FILE%_*}
        INDICES="${INDICES} ${INDEX}"
    done
    msg "New indices set: ${INDICES}"
fi

# determine suffix when arbitrary set
if [[ "${DATA_PERIOD}" == "day" ]]; then
    SUFFIX="-$(date +%Y-%m-%d)"
elif [[ "${DATA_PERIOD}" == "month" ]]; then
    SUFFIX="-$(date +%Y-%m)"
elif [[ "${DATA_PERIOD}" == "year" ]]; then
    SUFFIX="-$(date +%Y)"
elif [[ "${DATA_PERIOD}" == "all" ]]; then
    SUFFIX="-*"
elif [[ "${DATA_PERIOD}" == "" ]]; then
    error "import period not provided"
    exit 1
else
    SUFFIX="${DATA_PERIOD}"
fi

for INDEX in ${INDICES}; do
    # determine suffix when set by model
    if [[ "${DATA_PERIOD}" == "from_template" ]]; then
        get_suffix_from_template ${INDEX}
    fi
    update_index ${INDEX} ${SUFFIX}
done

msg "==== FINISH ====="
