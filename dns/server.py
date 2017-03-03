from multiprocessing import Process, Manager
from concurrent import futures
from socket import *
from pprint import pprint

import grpc

import dns_pb2
import dns_pb2_grpc

PORT = 50000  # GRPC server port


class InfoManager:
    @staticmethod
    def rotate_info(host_list):
        service = host_list.pop()
        host_list = [service] + host_list

        return service, host_list


class DNSInfo(dns_pb2_grpc.DNSInfoServicer):
    host_list = list()

    def InitConnection(self, *_):
        return dns_pb2.InitResponse(result=False)

    def InitInfo(self, request, _):
        host = request.host
        port = request.port
        print(f"[ {host}:{port} ] is connected")
        DNSInfo.host_list.append((host, port))
        print("Now Info Status: ")
        pprint(DNSInfo.host_list)

        return dns_pb2.InfoResponse(result=True)

    @staticmethod
    def rotate_host_list():
        service = DNSInfo.host_list.pop()
        DNSInfo.host_list = [service] + DNSInfo.host_list

        return service

    def RoundHost(self, *_):
        host, port = DNSInfo.rotate_host_list()
        return dns_pb2.HostResponse(host=host, port=port)


class DNSServer:
    def __init__(self, host='0.0.0.0', _port=8080):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind((host, _port))
        self.s.listen(100)
        self.info_manager = InfoManager()

        channel = grpc.insecure_channel("localhost:%d" % PORT)
        self.stub = dns_pb2_grpc.DNSInfoStub(channel)

    def get_host(self):
        resp = self.stub.RoundHost(dns_pb2.HostRequest(result=True))
        return resp.host, resp.port

    def run(self):
        while True:
            client, addr = self.s.accept()
            print(addr, " is connected at DNS")

            host_port = self.get_host()
            print("Redirect to: ", host_port)
            with socket(AF_INET, SOCK_STREAM) as s:
                s.connect(host_port)
                s.send(client.recv(4096))
                client.send(s.recv(4096))
                client.close()

    def done(self):
        self.s.close()


def run_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dns_pb2_grpc.add_DNSInfoServicer_to_server(DNSInfo(), server)
    server.add_insecure_port('[::]:%d' % PORT)
    server.start()
    print("Run GRPC Server!!")

    try:
        import time
        while True:
            time.sleep(100000)
    except KeyboardInterrupt:
        server.stop(0)


def run_dns_server():
    print("Run DNS Server!!")
    d = DNSServer()
    try:
        d.run()
    except KeyboardInterrupt:
        d.done()


def main():
    process_list = [Process(target=run_grpc_server),
                    Process(target=run_dns_server)]

    # run_grpc_server()
    # run_dns_server()

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()


if __name__ == '__main__':
    main()

"""

from multiprocessing import Process

def f(name):
    print 'hello', name

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()

"""
