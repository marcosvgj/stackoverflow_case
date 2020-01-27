STATUS_CODE=0
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_HOST=${POSTGRES_HOST}
POSTGRES_DB=${POSTGRES_DB}
SUPERSET_DB=${SUPERSET_DB}
SLEEP_TIME=${SLEEP_TIME}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
INJECTED_METADATA=${INJECTED_METADATA}

FAIL=1
echo "[Setup] - USER: ${POSTGRES_USER} HOST: ${POSTGRES_HOST} DATABASE: ${SUPERSET_DB} SLEEP: ${SLEEP_TIME}"
RESPONSE=$(psql -U ${POSTGRES_USER} -h postgres -d postgres -c "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'saved_query');" -Xt)

if [ $RESPONSE = 'f' ];then
    echo "Fail to connect to table public.saved_query"
    exit ${FAIL}
else
    echo "Connected successfully to table public.saved_query.  Inserting data"
    # [TODO] Review is needed     
    RESPONSE=$(PGPASSWORD="postgres" psql -U postgres -h postgres -d postgres -f ${INJECTED_METADATA} -Xt)
    if [ $? -eq 0 ];then
        echo "Success."
    fi
    exit $?
fi

