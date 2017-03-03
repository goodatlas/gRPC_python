#! /bin/bash
if [ -z ${VIRTUAL_ENV+x} ]; then
python3.6 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./*.proto
else
$VIRTUAL_ENV/bin/python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./*.proto
fi
