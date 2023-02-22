## introduction
This project includes simpe python scripts to run http api test, together with the gitlab-ci and docker files. 
## how to run tests in mac

### install dependencies
- In the project directory, you can run:
  `pip install -r requirements.txt`
- install Allure
  `brew install allure`
- install redis
  `brew install redis`  
 ### run tests
in command line, in the project directory, you can run:
  `python run.py`

## how to run tests in ubuntu
- install docker, docker-compose
- pull redis:5.0.0,latest nginx,grafana,influxdb images
- build python-allure from the Dockerfile in project dir
`docker build -t pyallure:v4 .`
- start docker container
`docker-compose up -d --force-recreate`
- run test
` docker exec -t your_container_name  /bin/bash -c "python run.py"`