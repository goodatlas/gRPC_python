# GRPC python <img src="https://circleci.com/gh/goodatlas/GRPC_python.svg?style=shield&circle-token=b626f406e33a287490f7cfc19a8ac363b702b0a0">

> After install `docker`.

## Build
```bash
bash$ make
```

## See Counter Log
```bash
bash$ make log
```

## See Frontend Log
```bash
bash$ make log_frontend
```

## Result
![1.png](./image/1.png)





## But..
there is some docker-sompose issue that related with ip address
- https://github.com/docker/compose/issues/4471
- http://stackoverflow.com/questions/35459262/how-to-set-static-ip-address-to-a-container-running-into-a-swarm-over-a-weave-ov
