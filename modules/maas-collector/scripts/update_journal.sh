#!/bin/bash
#set -x 

# init default values, use pods env if exists
ES_URL="${ES_URL:-http://localhost:9200}"
ES_USER="${ES_USERNAME:-admin}"
ES_PWD="${ES_PASSWORD:-admin}"
INDEX="maas-collector-journal" 
FIELD1="last_collect_date"
FIELD2="last_date"

## display usage help message 
function usage(){
    echo "$0"
    echo "  procedure options:"
    echo "   -e set full opensearch url (default http://localhost:9200)"
    echo "   -u set opensearch user (default admin)"
    echo "   -p set opensearch password (default admin)"
    echo "   -i set the indexe (defaultmaas-collector-journal )"
    echo "   --field1 set first field (default last_collect_date)"
    echo "   --field2 set second field (default last_date)"
    echo ""
    echo "samples :"
    echo ""
    echo "   set last_collect_date and last_date with default value" 
    echo "     $0 LTA_Werum 2021-12-15T08:30:00.549Z 2021-12-17T08:30:00.549Z"
    echo ""  
    echo "   set last_collect_date and last_date with default with all option activated"
    echo "     $0 -e http://localhost:9200 -u admin -p admin -i maas-collector-journal --field1=last_collect_date --field2=last_date LTA_Werum 2021-12-15T08:30:00.549Z 2021-12-17T08:30:00.549Z"
    echo ""
    echo "   set only last_collect_date  with default value" 
    echo "     $0 --field2=None LTA_Werum 2021-12-15T08:30:00.549Z"
    echo ""
    echo ""
}

# set options
while getopts "he:u:p:d:i:-:" opt; do
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
    i)
        INDEX="${OPTARG}"
    ;;
    -)
        case "${OPTARG%%=*}" in
            field1)
                OPT="${OPTARG%%=*}"
                OPTARG="${OPTARG#$OPT}"
                OPTARG="${OPTARG#=}"
                FIELD1="${OPTARG}"
            ;;
            field2)
                OPT="${OPTARG%%=*}"
                OPTARG="${OPTARG#$OPT}"
                OPTARG="${OPTARG#=}"
                FIELD2="${OPTARG}"
            ;;
        esac
    ;;
    \?)
        warn "Invalid option: -${OPTARG}" >&2
        usage
        exit
    ;;
    esac
done

shift $((OPTIND-1))

#check parameters
if [ -z "$1" ]
  then
    echo "No id arguments supplied"
    exit
fi

if [ -z "$2" ]
  then
    echo "No ${FIELDS1} arguments supplied"
    exit
fi

if [ ${FIELD1} != "None" ] && [ ${FIELD2} != "None" ]
  then
    if [ -z "$3" ]
      then
        echo "No ${FIELDS2} arguments supplied"
        exit
    fi
fi

# curl request
# example curl -XPOST -u admin:admin --header 'Content-Type: application/json' http://localhost:9200/maas-collector-journal/_update_by_query?pretty -d '{"query":{"term":{"_id":"LTA_Werum"}},"script":"ctx._source.last_collect_date=\"2021-12-15T08:30:00.549Z\";ctx._source.last_date=\"2021-12-15T08:30:00.549Z\""}'

QUERY=""

# create query
if [ ${FIELD1} != "None" ] && [ ${FIELD2} != "None" ]
then
    QUERY="'{\"query\":{\"term\":{\"_id\":\"$1\"}},\"script\":\"ctx._source.${FIELD1}=\\\"$2\\\";ctx._source.${FIELD2}=\\\"$3\\\" \"}'"
elif [ ${FIELD1} == "None" ] && [ ${FIELD2} != "None" ]
then
    QUERY="'{\"query\":{\"term\":{\"_id\":\"$1\"}},\"script\":\"ctx._source.${FIELD2}=\\\"$2\\\" \"}'"
elif [ ${FIELD1} != "None" ] && [ ${FIELD2} == "None" ]
then
    QUERY="'{\"query\":{\"term\":{\"_id\":\"$1\"}},\"script\":\"ctx._source.${FIELD1}=\\\"$2\\\" \"}'"
else
     echo "No ${FIELDS2} arguments supplied"
fi

# build curl arg
CONTENTTYPE="'Content-Type: application/json'"
CURLARGS="-s -XPOST -u ${ES_USER}:${ES_PWD} --header ${CONTENTTYPE} ${ES_URL}/${INDEX}/_update_by_query?pretty -d ${QUERY}"

# launch command curl

COMMAND="curl $CURLARGS"

OUTPUT=$(eval $COMMAND)

echo "$OUTPUT"



