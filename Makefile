default: all

all: \
	clean \
	build_docker \
	build_network \
	run \

build_docker:
	@docker build -t grpcpython -f Dockerfile .

build_network:
    @docker network create \
    --attachable=true \
    --gateway=172.25.0.1 \
    --ip-range=172.25.0.0/24 \
    --subnet=172.25.0.0/24 \
    --driver=overlay \
    mynet

clean:
	@echo "Clean"

run:
	@docker deploy --compose-file docker-compose.yaml grpcpython_stack

stop:
	@docker stack rm grpcpython_stack

log:
	@docker service logs -f grpcpython_stack_counter
