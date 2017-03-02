import os
import sys
from time import sleep

import grpc

import counter_pb2
import counter_pb2_grpc

from concurrent import futures

__ONE_DAY_BY_SECOND = 60 * 60 * 24
# HOST = '[::]'  # [::] is allow all host
PORT = 31337


class Counter(counter_pb2_grpc.CounterServicer):
    total_count = 0
    page_count = dict()

    @staticmethod
    def clear_screen():
        from sys import platform as _platform
        if _platform == 'win32':
            comm = 'cls'
        else:
            comm = 'clear'

        os.system(comm)

    @classmethod
    def print_data(cls):
        Counter.clear_screen()
        print("---------------------")
        print('Hits: %d' % cls.total_count)
        for page_name in cls.page_count.keys():
            print('%s: %d' % (page_name, cls.page_count[page_name]))
        print("---------------------")

    def Increment(self, request, _):
        Counter.total_count += 1
        try:
            Counter.page_count[request.name] += 1
        except KeyError:
            Counter.page_count[request.name] = 1

        self.print_data()

        return counter_pb2.IncrementResponse(count=Counter.total_count)

    @classmethod
    def total_page(cls):
        # wrap list()
        # because dict.keys() returns dict_keys type.
        return list(cls.page_count.keys())


def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    counter_pb2_grpc.add_CounterServicer_to_server(Counter(), server)
    server.add_insecure_port('%s:%d' % ("[::]", PORT))
    server.start()

    try:
        while True:
            sleep(__ONE_DAY_BY_SECOND)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run_server()
