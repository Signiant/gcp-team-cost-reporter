#!/usr/local/bin/bash

CONFIG_FILE=/my/folder/config.yaml
SERVICE_ACCOUNT_FILE=/my/folder/service-account.json

docker -H :4000 run -d -v ${CONFIG_FILE}:/config.yaml -v ${SERVICE_ACCOUNT_FILE}:/service-account.json signiant/gcp-team-cost-reporter -c /config.yaml
