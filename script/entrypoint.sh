#!/usr/bin/env bash


# Global defaults and back-compat
: "${AIRFLOW_HOME:="/opt/airflow"}"
: "${AIRFLOW__CORE__FERNET_KEY:=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")}"
: "${AIRFLOW__CORE__EXECUTOR:="SequentialExecutor"}"

export \
  AIRFLOW_HOME \
  AIRFLOW__CORE__EXECUTOR \
  AIRFLOW__CORE__FERNET_KEY \
  AIRFLOW__CORE__LOAD_EXAMPLES \
# Move to the AIRFLOW HOME directory
cd $AIRFLOW_HOME

# Initiliase the metadatabase
airflow db init

# Create User
airflow users create -e "admin@airflow.com" -f "airflow" -l "airflow" -p "airflow" -r "Admin" -u "airflow"

airflow scheduler & > /dev/null &

exec airflow webserver
