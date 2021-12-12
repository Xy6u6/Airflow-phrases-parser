FROM apache/airflow:latest-python3.8

ARG AIRFLOW_DEPS="slack"
ARG PYTHON_DEPS=""
# Export the environment variable AIRFLOW_HOME where airflow will be installed

ENV AIRFLOW_HOME=${AIRFLOW_HOME}
ENV PYTHONPATH "${PYTHONPATH}:${AIRFLOW_HOME}/dags/src"

# Install dependencies and tools
# Upgrade pip
# Create airflow user 
# Install apache airflow with subpackages


RUN pip install apache-airflow[kubernetes${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi


COPY requirements.txt requirements.txt
COPY credentials/gcp_acc.json $AIRFLOW_HOME/credentials/gcp_acc.json
COPY script/entrypoint.sh $AIRFLOW_HOME/script/entrypoint.sh
COPY dags/ $AIRFLOW_HOME/dags/

USER root
RUN chmod +x $AIRFLOW_HOME/script/entrypoint.sh
#RUN mkdir -m 777 "/tmp/parser"
RUN chown -R airflow: ${AIRFLOW_HOME}
#RUN chown -R airflow: /tmp/parser
USER airflow


RUN pip install -r requirements.txt

ENTRYPOINT ["./script/entrypoint.sh"]


