#!/bin/bash

superset db upgrade

superset fab create-admin \
            --username admin \
            --firstname Superset \
            --lastname Admin \
            --email admin@superset.com \
            --password ${ADMIN_PASSWORD:-admin}

superset init

if [ "${SUPERSET_SQLALCHEMY_EXAMPLES_URI}" = "iris://"* ]; then
    superset load-examples &
fi

/usr/bin/run-server.sh