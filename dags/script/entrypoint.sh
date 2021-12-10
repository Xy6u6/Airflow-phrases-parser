#!/usr/bin/env bash
# Move to the AIRFLOW HOME directory
cd $AIRFLOW_HOME

# Initiliase the metadatabase
airflow db init

# Create User
airflow users create -e "admin@airflow.com" -f "airflow" -l "airflow" -p "airflow" -r "Admin" -u "airflow"

airflow scheduler &

exec airflow webserver
