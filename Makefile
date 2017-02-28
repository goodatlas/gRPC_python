default: all

all: \
	clean \
	build \
	run \

build:
	@docker build -t grpcpython -f Dockerfile .


clean:
	@echo "Clean"

run:
	@docker deploy --compose-file docker-compose.yaml grpcpython_stack

stop:
	@docker stack rm grpcpython_stack

log:
	@docker service logs -f grpcpython_stack_counter
