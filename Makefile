default: all

all: \
	build_docker \
	run \

build_docker:
	@docker build -t grpcpython -f Dockerfile .

run:
	@docker deploy --compose-file docker-compose.yaml grpcpython_stack

stop:
	@docker stack rm grpcpython_stack

log:
	@docker service logs -f grpcpython_stack_counter
