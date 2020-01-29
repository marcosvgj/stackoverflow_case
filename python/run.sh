#!/usr/bin/env bash

# TITLE: run.sh
# DESCRIPTION: Spark Job entrypoint
# ============================================================================

set -e

exec python2 ${SPARK_APPLICATION_PYTHON_LOCATION}
STATUS_CODE=$?
if [$STATUS_CODE -eq 0];then
    echo "Worked!"
    exit $STATUS_CODE
else
    echo "Failed"
    exit 1
fi

