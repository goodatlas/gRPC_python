import sys
import grpc
from socket import *
from counter.server import PORT
from dns.server import PORT as dns_PORT
from counter import counter_pb2_grpc, counter_pb2
from dns import dns_pb2, dns_pb2_grpc
from grpc._channel import _Rendezvous


class WebApp:
    @staticmethod
    def get_host():
        import platform
        return platform.node()

    @staticmethod
    def get_ip():
        import subprocess
        output = subprocess.check_output("ifconfig | grep inet | grep 127", shell=True).decode()
        for obj in output.split(' '):
            if '127' in obj:
                return obj
        else:
            raise RuntimeError("There is no valid ip address")

    def __init__(self, name, s_host, s_port):

        self.name = WebApp.get_host() + '_' + name

        # for SOCKET
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.port = int(s_port)
        self.host = s_host
        self.ip_addr = self.get_ip()
        self.__bind_socket()
        self.__listen()

        counter_find = False
        dns_find = False

        # for find counter GRPC and DNS GRPC address
        for num in range(1, 255):
            ip = '172.25.0.%d' % num

            # kidding
            ip = 'localhost'

            print("Challenge %s" % ip)

            if counter_find is False:
                self.counter_stub = self.__setting_channel_stub(counter_pb2_grpc.CounterStub, ip, PORT)
                try:
                    self.test_counter_connection()
                except _Rendezvous:
                    pass
                else:
                    # print(self.name, " is find counter address by ", ip)
                    print(f"[ {self.name} ] find counter address: {ip}")
                    counter_find = True

            if dns_find is False:
                self.dns_stub = self.__setting_channel_stub(dns_pb2_grpc.DNSInfoStub, ip, dns_PORT)
                try:
                    self.test_dns_connection()
                except _Rendezvous:
                    raise
                else:
                    # print(self.name, " is find dns address by ", ip)
                    print(f"[ {self.name} ] find dns address: {ip}")
                    dns_find = True

            if counter_find and dns_find:
                break

        self.init_page()

    def test_counter_connection(self):
        self.counter_stub.InitConnection(counter_pb2.InitRequest(result=True))

    def test_dns_connection(self):
        self.dns_stub.InitConnection(dns_pb2.InitRequest(result=True))

    def add_dns(self):
        self.dns_stub.InitInfo(dns_pb2.InfoRequest(host=self.ip_addr, port=self.port))

    def increment_count(self):
        return self.counter_stub.Increment(counter_pb2.IncrementRequest(name=self.name))

    def init_page(self):
        self.add_dns()
        self.counter_stub.InitPage(counter_pb2.InitPageRequest(name=self.name))

    @staticmethod
    def __setting_channel_stub(stub_func, ip, port):
        print(ip, port, " connecting")
        channel = grpc.insecure_channel('%s:%d' % (ip, port))
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
    try:
        w = WebApp(sys.argv[1], sys.argv[2], sys.argv[3])
        w.run()
    except IndexError:
        print("Usage: %s [app name] [host] [port]" % sys.argv[0])
    except KeyboardInterrupt:
        w.done()
    else:
        print("Good.")
