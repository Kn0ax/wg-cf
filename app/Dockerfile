# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
#RUN apk update
#RUN apk add py3-gunicorn
RUN adduser -D n3on
USER n3on
WORKDIR /home/n3on/app
COPY requirements.txt /home/n3on/app/
COPY gunicorn.sh /home/n3on/app/
RUN python3 -m pip install -r /home/n3on/app/requirements.txt
COPY . /home/n3on/app

CMD sh gunicorn.sh