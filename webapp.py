import grpc

from socket import *

from counter.counter_pb2 import IncrementRequest
from counter.counter_pb2_grpc import CounterStub

ONE_DAY_BY_SECOND = 60 * 60 * 24


class WebApp:
    @staticmethod
    def get_host():
        import platform
        return platform.node()

    def set_channel_stub(self, upstreamaddr, channel_options = None):
        channel = grpc.insecure_channel(upstreamaddr, channel_options)
        self.stub = CounterStub(channel)

    def increase_count(self, name=None):
        if name is None:
            name = self.host_name
        return self.stub.Increment(IncrementRequest(name=name))

    def bind(self, bind_addr, backlog=5, reuse=True):

        if self.s is None:
            self.s = socket(AF_INET, SOCK_STREAM)

        if reuse:
            self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        host, port = bind_addr.split(':')

        self.s.bind((host, int(port)))
        self.s.listen(backlog)

    def __init__(self, name, upstream_addr, bind_addr, channel_options = None):
        self.name = name
        self.bind_addr = bind_addr
        self.upstream_addr = upstream_addr

        self.s = None
        self.host_name = (WebApp.get_host() + '_' + name)
        self.stub = None

        self.set_channel_stub(upstream_addr, channel_options)

    def start(self):
        raise NotImplementedError('Method not implemented!')
