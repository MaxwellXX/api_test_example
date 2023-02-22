FROM ubuntu:18.04
# HAVE TO USE PROXY SUCH AS CLASH WHEN RE-BUILDING IMAGE,
# OR psycopg2==2.8.6 CANNOT BE DOWNLOADED(Will be much slower ^_^)
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

RUN apt-get update && \
    apt-get install --assume-yes apt-utils && \
    apt-get install -y locales && \
    locale-gen en_US.UTF-8

RUN apt-get install -y software-properties-common vim

# install postgres, REPO monitoring scripts use psycopg2 to connect to postgresql, and this package depends on postgresql
RUN apt-get update --fix-missing && apt-get install -y postgresql && \
    apt-get install -y python-psycopg2  && \
    apt-get install -y libpq-dev

# install python3.6
RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv && \
    apt-get install -y git

RUN ln -sfn /usr/bin/python3.6 /usr/bin/python

# update pip, use douban source ot it will time out~~https://pypi.tuna.tsinghua.edu.cn/simple source is OK too
RUN python3 -m pip install -i https://pypi.doubanio.com/simple/ pip --upgrade && \
    python3 -m pip install -i https://pypi.doubanio.com/simple/ wheel

# install allure, does not work using apt get, use curl instead
#RUN apt-add-repository ppa:qameta/allure
#RUN apt-get install -y allure

RUN apt install -y curl
RUN apt-get install -y openjdk-8-jdk
RUN curl -o allure-2.7.0.tgz -Ls https://dl.bintray.com/qameta/generic/io/qameta/allure/allure/2.7.0/allure-2.7.0.tgz && tar -zxvf allure-2.7.0.tgz -C /opt/ && ln -s /opt/allure-2.7.0/bin/allure /usr/bin/allure && allure --version

# install python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt  -i https://pypi.doubanio.com/simple && \
    pip3 install --no-cache-dir psycopg2==2.8.6