#!/usr/bin/env bash
hdfs dfs -mkdir -p    /user/airflow/
hdfs dfs -chmod g+w   /user/airflow
# Move to the AIRFLOW HOME directory
cd $AIRFLOW_HOME

# Initiliase the metadatabase
airflow db init

# Create User
airflow users create -e "admin@airflow.com" -f "airflow" -l "airflow" -p "airflow" -r "Admin" -u "airflow"

airflow scheduler &> /dev/null &

exec airflow webserver
