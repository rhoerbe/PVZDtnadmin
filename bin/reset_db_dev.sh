#!/usr/bin/env bash

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
APPHOME=$(dirname $scriptsdir)
source $scriptsdir/setenv.sh
export DJANGO_SETTINGS_MODULE=pvzdweb.settings_dev

ssh devl11 /home/r2h2/devl/docker/c-pvzdweb-pg-dev/reset_pg_data.sh
sleep 2 && wait_pg_become_ready.sh

$APPHOME/manage.py migrate
#manage.py createsuperuser --email rainer@hoerbe.at
$APPHOME/bin/load_testdata.sh