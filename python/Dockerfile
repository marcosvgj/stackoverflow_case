FROM openjdk:8-alpine

ARG MODEL_PATH
ARG USED_JAR_PATH

ENV MODEL_PATH=${MODEL_PATH}
ENV USED_JAR_PATH=${USED_JAR_PATH}
ENV MODEL_PATH='model.models'
ENV USED_JAR_PATH='/jars/postgresql-9.4.1207.jre6.jar'

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

COPY /jars /jars
COPY /src /src
COPY /requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY /jars /jars

WORKDIR /src


