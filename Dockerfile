FROM ubuntu

WORKDIR /grpc_python/requirements

RUN apt-get update
RUN apt-get install -y python-software-properties software-properties-common python-dev python3-dev gcc build-essential g++ net-tools
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install python3.6 -y
RUN apt-get install -y libpython3.6-dev

RUN python3.6 get-pip.py
RUN python3.6 -m pip install -r requirements.txt

ADD counter /grpc_python/counter
ADD dns /grpc_python/dns
ADD web.py /grpc_python/web.py
ADD requirements /grpc_python/requirements

WORKDIR /grpc_python
