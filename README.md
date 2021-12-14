# Airflow-phrases-parser
Steps to run:
1 - clone repo:

      git clone git@github.com:Xy6u6/Airflow-phrases-parser.git
      
2 - Type in terminal to create a tmp dir for files

     mkdir -p -m 777 /tmp/parser/

3 - create json file with creds to connect to GCP 

    mkdir -p Airflow-phrases-parser/credentials/ && touch $_/gcp_acc.json
3 - run
    docker-compose up --build
4 - visit localhost:8080 to monitor workflow
5 - test if works in /tmp/parser/ or in GCS "gs://phrases-parser" bucket name and 