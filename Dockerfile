# Base Image
FROM apache/airflow:2.1.2-python3.8

# Arguments that can be set with docker build
ARG AIRFLOW_VERSION=2.1.2
ARG PYTHON_VERSION=3.8
ARG AIRFLOW_HOME=/opt/airflow

# Export the environment variable AIRFLOW_HOME where airflow will be installed
ENV AIRFLOW_HOME=${AIRFLOW_HOME}
ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow/dags/src"
# Install dependencies and tools
# Upgrade pip
# Create airflow user 
# Install apache airflow with subpackages
RUN pip install apache-airflow==${AIRFLOW_VERSION};

COPY requirements.txt .
COPY gcp_acc.json ./tmp/gcp_acc.json
COPY dags/script/entrypoint.sh /entrypoint.sh
COPY dags/ $AIRFLOW_HOME/dags/

USER root
RUN chmod +x /entrypoint.sh
USER airflow

RUN pip install -r requirements.txt


ENTRYPOINT ["/entrypoint.sh"]

    