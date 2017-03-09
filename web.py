from socket import *

import grpc

from counter import counter_pb2_grpc, counter_pb2


class WebApp:
    @staticmethod
    def get_host():
        import platform
        return platform.node()

    @staticmethod
    def get_ip():
        import subprocess
        output = subprocess.check_output("ifconfig | grep 10.0", shell=True).decode()

        for obj in output.split(' '):
            if 'addr' in obj:
                return obj.split(':')[1]
        else:
            raise RuntimeError("There is no valid ip address")

    def __init__(self, name, s_host, s_port, counter_info, dns_info):

        self.name = WebApp.get_host() + '_' + name

        self.host = s_host
        self.port = int(s_port)
        self.ip_addr = self.get_ip()

        print("my ip: ", self.ip_addr)

        print("counter info: ", counter_info)
        print("dns info: ", dns_info)

        self.counter_stub = counter_pb2_grpc.CounterStub(grpc.insecure_channel(counter_info))

        # for SOCKET
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.__bind_socket()
        self.__listen()

    def increment_count(self):
        return self.counter_stub.Increment(counter_pb2.IncrementRequest(name=self.name))

    @staticmethod
    def __setting_channel_stub(stub_func, channel):
        stub = stub_func(channel)

        return stub

    def __bind_socket(self, reuse=True):
        if reuse:
            self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.socket.bind((self.host, self.port))

    def __listen(self, backlog=100):
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
            self.send('%s is handling. count: %s' % (self.name, self.increment_count()), socket=client)
            client.close()

    def done(self):
        self.socket.close()
        print("Server Closed")


if __name__ == '__main__':
    import sys

    try:
        w = WebApp(sys.argv[1], sys.argv[2], sys.argv[3])
        w.run()
    except IndexError:
        print("Usage: %s [app name] [host] [port]" % sys.argv[0])
    except KeyboardInterrupt:
        w.done()
    else:
        print("Good.")
