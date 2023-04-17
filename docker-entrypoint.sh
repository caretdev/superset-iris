#!/bin/bash

superset fab create-admin \
            --username admin \
            --firstname Superset \
            --lastname Admin \
            --email admin@superset.com \
            --password ${ADMIN_PASSWORD:-admin}

superset db upgrade

superset init

/usr/bin/run-server.sh