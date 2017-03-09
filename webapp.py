import grpc
from counter.counter_pb2 import IncrementRequest
from counter.counter_pb2_grpc import CounterStub


class WebApp:
    @staticmethod
    def get_host():
        import platform
        return platform.node()

    def __set_channel_stub(self, upstreamaddr):
        channel = grpc.insecure_channel(upstreamaddr)
        self.stub = CounterStub(channel)

    def __increase_count(self):
        return self.stub.Increment(IncrementRequest(name=self.name))

    def __init__(self):
        self.name = Web.get_host()
        self.stub = None
