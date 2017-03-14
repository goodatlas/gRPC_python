# -*- coding: utf-8 -*-
# For Running Terminal
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

# Module for Test
import random
import unittest

# grpc_python module
from counter.counter_pb2 import IncrementRequest
from counter.server import run_server
from frontend import Frontend
from proxy import Proxy

# process manage module
import signal

# Module For gRPC
import grpc
from counter.counter_pb2_grpc import CounterStub

from multiprocessing import Process


dnslb = [('grpc.lb_policy_name', 'round_robin')]


def run_frontend_server(proxy_port, frontend_port):
    f = Frontend('frontend', f'localhost:{proxy_port}', f'localhost:{frontend_port}', dnslb)
    f.start()


def run_proxy_server(counter_port, proxy_port):
    p = Proxy('proxy', f'localhost:{counter_port}', f'localhost:{proxy_port}')
    p.start()


def run_counter_server(counter_port):
    run_server(f'localhost:{counter_port}')


def get_function_name(func):
    def wrapper(self, *args, **kwargs):
        return func(self, func.__name__, *args, **kwargs)

    return wrapper


class GRPCTest(unittest.TestCase):
    all_process = list()

    def setUp(self):
        self.frontend_port, self.proxy_port, self.counter_port = random.sample(range(50000, 55000), 3)
        self.proxy_process = Process(target=run_proxy_server, args=(self.counter_port, self.proxy_port))
        self.counter_process = Process(target=run_counter_server, args=(self.counter_port,))

        self.proxy_process.start()
        self.counter_process.start()

        self.__class__.all_process += [self.proxy_process, self.counter_process]

        # Be sure to running server done
        import time
        time.sleep(1)

        self.counter_stub = CounterStub(grpc.insecure_channel(f"localhost:{self.counter_port}"))
        self.proxy_stub = CounterStub(grpc.insecure_channel(f"localhost:{self.proxy_port}"))

    @classmethod
    def tearDownClass(cls):
        print("Done!")
        for process in cls.all_process:
            os.kill(process.pid, signal.SIGTERM)

    @get_function_name
    def test_grpc(self, func_name):
        result = self.proxy_stub.Increment(IncrementRequest(name=func_name))
        self.assertNotEqual(result.count, None)


if __name__ == "__main__":
    unittest.main()

    # Things TODO
    # - GRPC Test
    # -- from Proxy, to Counter
    # -- from Frontend, to Proxy
    # - Web Request Test
    # -- from client, to Frontend with HTTP
