from concurrent import futures
from time import sleep

import sys
import grpc

from webapp import WebApp, ONE_DAY_BY_SECOND
from counter.counter_pb2_grpc import CounterServicer, add_CounterServicer_to_server
from counter.counter_pb2 import IncrementResponse


class Proxy(WebApp, CounterServicer):
    def Increment(self, request, _):
        frontend_name = request.name
        self.increase_count()
        return IncrementResponse(count=self.increase_count(frontend_name).count)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_CounterServicer_to_server(Proxy(self.name, self.upstream_addr, self.bind_addr), server)
        server.add_insecure_port(self.bind_addr)
        server.start()
        sys.stdout.write('Proxy Starts at %s\n' % str(self.bind_addr))

        try:
            while True:
                sleep(ONE_DAY_BY_SECOND)
        except KeyboardInterrupt:
            server.stop(0)

