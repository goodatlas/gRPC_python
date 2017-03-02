import sys
import grpc
from socket import *
from counter.server import HOST, PORT
from counter import counter_pb2_grpc, counter_pb2


class WebApp:
    def __init__(self, name, s_host='localhost', s_port=8080):
        self.name = name

        # for SOCKET
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.port = s_port
        self.host = s_host
        self.__bind_socket()
        self.__listen()

        # for GRPC
        self.channel, self.stub = self.__setting_channel_stub()

    def increment_count(self):
        return self.stub.Increment(counter_pb2.IncrementRequest(name=self.name))

    @staticmethod
    def __setting_channel_stub():
        channel = grpc.insecure_channel('%s:%d' % (HOST, PORT))
        stub = counter_pb2_grpc.CounterStub(channel)

        return channel, stub

    def __bind_socket(self, reuse=True):
        if reuse:
            self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.socket.bind((self.host, self.port))

    def __listen(self, backlog=5):
        self.socket.listen(backlog)

    def send(self, data, socket=None):
        if socket is None:
            socket = self.socket
        print("Send %s" % data)
        socket.send(data.encode('utf-8'))

    def run(self):
        print("Wait connection at %s:%d" % (self.host, self.port))
        while True:
            client, addr = self.socket.accept()
            client.recv(1024)
            # addr is tuple.
            # len(addr) == 2
            print("%s:%s is connected" % addr)
            self.send('%s is handling. count: %s' % (self.name, self.increment_count()), client)
            client.close()

    def done(self):
        self.socket.close()
        print("Server Closed")


if __name__ == '__main__':
    try:
        w = WebApp(sys.argv[1])
        w.run()
    except IndexError:
        print("Usage: %s [app name]" % sys.argv[0])
    except KeyboardInterrupt:
        w.done()
    else:
        print("Good.")
