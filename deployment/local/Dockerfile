# This is a simple Dockerfile to use while developing
# It's not suitable for production
#
# for django: docker run --env-file=.env image django run

# pull official base image
FROM python:3.9.15-alpine

# set work directory
RUN mkdir /task_manager_api
WORKDIR /task_manager_api

COPY ./ /task_manager_api

# Install or update pip
RUN pip install --upgrade pip

# Set environment variables for MySQL client
ENV MYSQLCLIENT_CFLAGS "-I/usr/local/Cellar/mysql/8.0.32/include/mysql"
ENV MYSQLCLIENT_LDFLAGS "-L/usr/local/Cellar/mysql/8.0.32/lib -lmysqlclient -lz -L/usr/local/lib -lzstd -L/usr/local/opt/openssl@1.1/lib -lssl -lcrypto -lresolv"

# Optionally, set environment variables for psycopg2 (if needed)
ENV PG_CONFIG "/usr/local/bin/pg_config"  # Adjust the path as needed


## install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev libressl-dev postgresql-dev mysql-dev curl bash sudo

COPY requirements.txt ./

ADD requirements.txt /task_manager_api/
RUN pip install -r requirements.txt

ADD . /task_manager_api/


COPY ./deployment/local/start start
RUN sed -i 's/\r$//g' start
RUN chmod +x start

ENTRYPOINT ["/task_manager_api/start"]
