#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
RESOURCE_DIR="${PARENT_DIR}/resources"
#source lib functions
. ${SCRIPT_DIR}/functions.sh

## init default values 
ELASTIC_BASE_URL="http://localhost:9200"
ELASTIC_AUTH="admin:admin"
IGNORE_CERT="-k"
HEADER=""
ACTION=""
DOMAIN=""
ITEM=""
JSON_FILE=""
MODE=""
MODE=""
GEN_UUID=""
PRETTY=""
SILENT="--silent" 

## message for missing Action 
function missingAction(){
    warn "Missing Action : -A" >&2
    info " use one of:"
    info "  -A DISPLAY (display domain instances)"
    info "  -A SEARCH (search for item) elastic query stored in file (-d file)"
    info "  -A DELETE (delete an item)"
    info "  -A POPULATE (add item(s) data stored in file (-d file))"
    info "$0 -h for help"
    exit
}

## message for missing Domain
function missingDomain(){
    warn "Missing Domain : -D"
    info " use one of:"
    info "  -D TEMPLATES (templates)"
    info "  -D INDEX (indices)"
    info "$0 -h for help"
    exit
}

## compose search curl options
function search(){
    if [[ $JSON_FILE = "" ]]; then
        METHOD='-X GET'
        DATA=""
        HEADER=''
    else
        METHOD='-X POST'
        DATA_OPT="--data"
        DATA="@${JSON_FILE}"
        HEADER='-H Content-Type:application/json'
    fi
    if [[ ${ITEM} == "" ]]; then
        error "Item is missing"
    else
        case ${DOMAIN} in
        "TEMPLATE")
            warn "No search on template allowed"
            exit
            ;;
        "INDEX")
            ELASTIC_URL=${ELASTIC_BASE_URL}/${ITEM}/_search
            ;;
        *)
            missingDomain
        ;;
        esac
        docurl
    fi
}

## compose seadisplayrch curl options
function display(){
    METHOD='-X GET'
    DATA=""
    if [[ ${ITEM} == "" ]]; then
        case ${DOMAIN} in
        "TEMPLATE")
            ELASTIC_URL=${ELASTIC_BASE_URL}/_template
            ;;
        "INDEX")
            ELASTIC_URL=${ELASTIC_BASE_URL}/_aliases
            ;;
        *)
            missingDomain
        ;;
        esac
        docurl
    else
        case ${DOMAIN} in
        "TEMPLATE")
            ELASTIC_URL=${ELASTIC_BASE_URL}/_template/${ITEM}
            ;;
        "INDEX")
            ELASTIC_URL=${ELASTIC_BASE_URL}/${ITEM}
            ;;
        *)
            missingDomain
        ;;
        esac
        docurl
    fi
}

## compose delete curl options
function delete(){
    DATA=""
    if [[ ${ITEM} == "" ]]; then
        error "missing Item arg"
        exit
    else
        METHOD='-X DELETE'
        case ${DOMAIN} in
        "TEMPLATE")
            ELASTIC_URL=${ELASTIC_BASE_URL}/_template/${ITEM}
            ;;
        "INDEX")
            ELASTIC_URL=${ELASTIC_BASE_URL}/${ITEM}
            ;;
        *)
            missingDomain
        ;;
        esac
        docurl
    fi
}

## compose init curl options
function init(){
    DATA=""
    if [[ ${ITEM} == "" ]]; then
        error "missing Item arg"
        exit
    else
        METHOD='-X PUT'
        case ${DOMAIN} in
        "TEMPLATE")
            ELASTIC_URL=${ELASTIC_BASE_URL}/_template/${ITEM}
            ;;
        "INDEX")
            ELASTIC_URL=${ELASTIC_BASE_URL}/${ITEM}
            ;;
        *)
            missingDomain
        ;;
        esac
        docurl
    fi
}

## compose populate curl options
function populate(){
    METHOD='-X POST'
    HEADER='-H Content-Type:application/json'
    if [[ ${ITEM} == "" ]]; then
        error "missing Item arg"
        exit
    elif [[ ${JSON_FILE} == "" ]]; then
        error "missing input file arg"
        exit
    else
        case ${DOMAIN} in
        "TEMPLATE")
            ELASTIC_URL=${ELASTIC_BASE_URL}/_template/${ITEM}
            DATA_OPT="--data"
            DATA="@${JSON_FILE}"
            docurl
        ;;
        "INDEX")
            case ${MODE} in
            "BULK") 
                ELASTIC_URL=${ELASTIC_BASE_URL}/${ITEM}/_bulk?refresh=true
                DATA_OPT="--data-binary"
                DATA="@${JSON_FILE}"
                docurl
            ;;
            "ARRAY")
                for ROW in $(jq -r '.[] | @base64' ${JSON_FILE}); do
                    UUIDGEN=""
                    if [[ ${GEN_UUID} == "true" ]]; then
                        UUIDGEN="/"$(uuidgen)
                    fi
                    ELASTIC_URL=${ELASTIC_BASE_URL}/${ITEM}/_doc${UUIDGEN}
                    DATA_OPT="--data"
                    DATA=$(echo ${ROW} | base64 --decode)
                    docurl
                done
            ;;
            *)
                ELASTIC_URL=${ELASTIC_BASE_URL}/${ITEM}
                DATA_OPT="--data"
                DATA="@${JSON_FILE}"
                docurl
            ;;
            esac
        ;;
        *)
            missingDomain
        ;;
        esac
    fi
}

## launch curl command
function docurl(){
    if [[ ${DATA} != "" ]] ; then
        if [[ ${NO_EXECUTE} != "true" ]] ; then
            debug "curl ${SILENT} ${CURL_AUTH} ${IGNORE_CERT} ${METHOD} ${HEADER} ${ELASTIC_URL}${PRETTY} ${DATA_OPT} \"${DATA}\""
            curl ${SILENT} ${CURL_AUTH} ${IGNORE_CERT} ${METHOD} ${HEADER} ${ELASTIC_URL}${PRETTY} ${DATA_OPT} "${DATA}"
        else
            msg "curl ${SILENT} ${CURL_AUTH} ${IGNORE_CERT} ${METHOD} ${HEADER} ${ELASTIC_URL}${PRETTY} ${DATA_OPT} \"${DATA}\""        
        fi
    else
        if [[ ${NO_EXECUTE} != "true" ]] ; then
            debug "curl ${SILENT} ${CURL_AUTH} ${IGNORE_CERT} ${METHOD} ${HEADER} ${ELASTIC_URL}${PRETTY}"
            curl ${SILENT} ${CURL_AUTH} ${IGNORE_CERT} ${METHOD} ${HEADER} ${ELASTIC_URL}${PRETTY}
        else
            msg "curl ${SILENT} ${CURL_AUTH} ${IGNORE_CERT} ${METHOD} ${HEADER} ${ELASTIC_URL}${PRETTY}"

        fi
    fi
}

## display usage help message 
function usage(){
    echo "$0 Wrapper for elastic search ..."
    echo "usage :"
    echo ""
    echo "$0 hD:A:I:d:bjgpvne:a:"
    echo "  General options:"
    echo "   -h print this help"
    echo "   -v verbose mode"
    echo "   -n no exec mode (does not launch curl)"
    echo ""
    echo "  URL options:"
    echo "   -e set full opensearchpy url (default http://localhost:9200)"
    echo "   -a set opensearchpy auth (default admin:XXXXXXXXX)"
    echo ""
    echo "  Elastic options:"
    echo "   -D domain on of TEMPLATE, INDEX execute commands for template or indices"
    echo "   -A action on of DISPLAY, DELETE, SEARCH, INIT or POPULATE for display, delete, search, init or populate the selected domain"
    echo "       For POPULATE or SEARCH data, elastic request should be provided via a file using -d option"
    echo "   -I the choosen item (ie a specific template or indice name) if setted display, delete,search populate are applied on this item"
    echo "   -d the file path to the json handeling the content for template, search query, data or data bulk" 
    echo "   -b elastic bulk mode the given file to populate index is an elastic bulk file see produced_datastrip_export.bulk (bulk file is a dump)"
    echo "   -j json array mode the given file to populate index is an json array file see produced_datastrip_export.json"
    echo "   -g generate an uuid in array mode the uuid could be generated"
    echo "   -p format answer set pretty"
    echo ""
    echo "samples :"
    echo ""
    echo "  TEMPLATES:"
    echo "   display all templates :"
    echo "     $0 -v -D TEMPLATE -A DISPLAY -p"
    echo "   display a given template:"
    echo "     $0 -v -D TEMPLATE -A DISPLAY -I template_datastrip -p"
    echo "   delete a given template:"
    echo "     $0 -v -D TEMPLATE -A DELETE -I template_datastrip -p"
    echo "   init a given template:"
    echo "     $0 -v -D TEMPLATE -A INIT -I template_datastrip -p"
    echo "   populate a given template:"
    echo "     $0 -v -D TEMPLATE -A POPULATE -I template_datastrip -p -d ${RESOURCE_DIR}/datastrip_template.json"
    echo ""
    echo "  INDICES:"
    echo "   display all aliases :"
    echo "     $0 -v -D INDEX -A DISPLAY -p"
    echo "   display a given index:"
    echo "     $0 -v -D INDEX -A DISPLAY -I produced_datastrip -p"
    echo "   delete a given index:"
    echo "     $0 -v -D INDEX -A DELETE -I produced_datastrip -p"
    echo "   init a given index:"
    echo "     $0 -v -D INDEX -A INIT -I produced_datastrip -p"
    echo "   populate a given index with bulk data:"
    echo "     $0 -v -D INDEX -A POPULATE -I produced_datastrip -b -p -d ${RESOURCE_DIR}/produced_datastrip_export.bulk"
    echo "   populate a given index with json array data:"
    echo "     $0 -v -D INDEX -A POPULATE -I produced_datastrip -j -p -d ${RESOURCE_DIR}/produced_datastrip_export.json"
    echo "   search on a given index with json elastic querry:"
    echo "     $0 -v -D INDEX -A SEARCH -I produced_datastrip -p -d ${RESOURCE_DIR}/search_all.json"
}

# set options
while getopts "hD:A:I:d:bjgpvne:a:" opt; do
    case $opt in
    h)
        usage
        exit 1
        ;;
    A)
        ACTION="${OPTARG}"
        ;;
    D)
        DOMAIN="${OPTARG}"
        ;;
    I)
        ITEM="${OPTARG}"
        ;;
    d)
        JSON_FILE="${OPTARG}"
        ;;
    b)
        MODE="BULK"
        ;;
    j)
        MODE="ARRAY"
        ;;
    g)
        GEN_UUID="true"
        ;;
    p)
        #PRETTY="?pretty=true"
        ;;
    v)
        VERBOSE="true"
        ;;
    n)
        NO_EXECUTE="true"
        ;;
    e)
        ELASTIC_BASE_URL="${OPTARG}"
        ;;
    a)
        ELASTIC_AUTH="${OPTARG}"
        ;;
    \?)
        echo "Invalid option: -$OPTARG" >&2
        usage
        exit
        ;;
    esac
done

# handle authentication
if [[ -z ${ELASTIC_AUTH} ]] ; then
    CURL_AUTH=""
else
    CURL_AUTH="-u ${ELASTIC_AUTH}"
fi

## main
case ${ACTION} in
"DISPLAY")
    display
;;
"SEARCH")
    search
;;
"DELETE")
    delete
;;
"INIT")
    init
;;
"POPULATE")
    populate
;;
*)
    missingAction
;;
esac


