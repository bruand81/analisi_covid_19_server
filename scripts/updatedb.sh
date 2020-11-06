#!/bin/bash
# Django project directory
DJANGODIR=/home/antarescloud/analisi_covid_19_server
# which settings file should Django use
DJANGO_SETTINGS_MODULE=analisi_covid_19_server.settingsprod
# WSGI module name
DJANGO_WSGI_MODULE=analisi_covid_19_server.wsgi

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

python3 ${DJANGODIR}/manage.py update_db_from_csv