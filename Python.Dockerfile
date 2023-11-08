FROM python:3.11-alpine3.18

RUN apk add build-base
RUN apk --no-cache add tzdata

WORKDIR /home/app

RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ADD requirements.txt .
RUN python3 -m pip install --upgrade pip setuptools-scm wheel
RUN python3 -m pip install -r requirements.txt

ADD . /home/app
