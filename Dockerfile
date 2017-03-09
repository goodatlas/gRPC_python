FROM python:3.6-alpine

RUN echo 'http://dl-cdn.alpinelinux.org/alpine/edge/main' >> /etc/apk/repositories

RUN apk update

ADD requirements /grpc_python/requirements
WORKDIR /grpc_python/requirements
RUN python get-pip.py


RUN apk add --no-cache \
    python3-dev=3.6.0-r0 \
    bash \
    python-dev \
    gcc \
    g++ \
    libc6-compat \
    build-base \
    linux-headers \
    make \
    musl-dev \
    libffi \
    libffi-dev \
    && rm -rf /var/cache/apk/*

ADD counter /grpc_python/counter
ADD dns /grpc_python/dns
ADD web.py /grpc_python/web.py

RUN python -m pip install -r requirements.txt

WORKDIR /grpc_python

RUN export TERM=xterm