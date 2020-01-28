
#!/usr/bin/env bash

# TITLE: load_superset_metadata.sh
# DESCRIPTION: Used to Data insert failover to Apache Superset Metadata - Queries
# ============================================================================

SUCCESS=0
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_HOST=${POSTGRES_HOST}
POSTGRES_DB=${POSTGRES_DB}
SUPERSET_DB=${SUPERSET_DB}
SLEEP_TIME=${SLEEP_TIME}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
INJECTED_METADATA=${INJECTED_METADATA}

FAILURE_STAGE_MESSAGE="Fail to connect to table public.saved_query."
SUCCESS_STAGE_MESSAGE="Connected successfully to table public.saved_query. Inserting data..."
SUCCESS_MESSAGE="Insertion completed with success.."
FAILURE_MESSAGE="Failed to inject superset metadata"

FAIL=1
echo "[Setup] - USER: ${POSTGRES_USER} HOST: ${POSTGRES_HOST} DATABASE: ${SUPERSET_DB}"
QUERY="SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'saved_query' );"
RESPONSE_RULE_1=$(PGPASSWORD="${POSTGRES_PASSWORD}" psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -d ${POSTGRES_DB} -c "${QUERY}" -Xt || echo 'f')

QUERY="SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'dbs' );"
RESPONSE_RULE_2=$(PGPASSWORD="${POSTGRES_PASSWORD}" psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -d ${POSTGRES_DB} -c "${QUERY}" -Xt || echo 'f')

QUERY="SELECT COUNT(*) FROM public.dbs"
RESPONSE_RULE_3=$(PGPASSWORD="${POSTGRES_PASSWORD}" psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -d ${POSTGRES_DB} -c "${QUERY}" -Xt || echo 0 )

if [ ${RESPONSE_RULE_1} = 't' ] && [ ${RESPONSE_RULE_2} = 't' ];then
    if [ ${RESPONSE_RULE_3} -gt 0 ];then
        echo ${SUCCESS_STAGE_MESSAGE}
        if [ -z ${INJECTED_METADATA} ];then
            INJECTED_METADATA=/tmp/init_superset.sql
        fi 
        PGPASSWORD="${POSTGRES_PASSWORD}" psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -d ${POSTGRES_DB} --file ${INJECTED_METADATA} -Xt 1>/dev/null
        QUERY="SELECT COUNT(*) FROM public.saved_query"
        RESPONSE_RULE_4=$(PGPASSWORD="${POSTGRES_PASSWORD}" psql -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -d ${POSTGRES_DB} -c "${QUERY}" -Xt || echo 0 )
        if [ ${RESPONSE_RULE_4} -gt 0 ];then
            echo "${SUCCESS_MESSAGE}"
            exit ${SUCCESS}
        else
            echo ${FAILURE_STAGE_MESSAGE}
            exit ${FAIL}
        fi    
    else
        echo ${FAILURE_MESSAGE}
        exit ${FAIL}
    fi
else
    echo ${FAILURE_MESSAGE}
    exit ${FAIL}
fi