#! /bin/bash
$VIRTUAL_ENV/bin/python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./counter.proto