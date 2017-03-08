from socket import *

import grpc

from counter import counter_pb2_grpc, counter_pb2
from dns import dns_pb2, dns_pb2_grpc


class WebApp:
    @staticmethod
    def get_host():
        import platform
        return platform.node()

    @staticmethod
    def get_ip():
        import subprocess
        output = subprocess.check_output("ifconfig | grep 172", shell=True).decode()

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
        self.dns_stub = dns_pb2_grpc.DNSInfoStub(grpc.insecure_channel(dns_info))

        self.add_dns()
        self.init_page()

        # for SOCKET
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.__bind_socket()
        self.__listen()

    def test_counter_connection(self):
        self.counter_stub.InitConnection(counter_pb2.InitRequest(result=True))

    def test_dns_connection(self):
        self.dns_stub.InitConnection(dns_pb2.InitRequest(result=True))

    def add_dns(self):
        self.dns_stub.InitInfo(dns_pb2.InfoRequest(host=self.ip_addr, port=self.port))

    def increment_count(self):
        return self.counter_stub.Increment(counter_pb2.IncrementRequest(name=self.name))

    def init_page(self):
        self.counter_stub.InitPage(counter_pb2.InitPageRequest(name=self.name))

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
