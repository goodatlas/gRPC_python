import os
import sys
from concurrent import futures
from time import sleep

import counter_pb2
import counter_pb2_grpc
import grpc

__ONE_DAY_BY_SECOND = 60 * 60 * 24


# HOST = '[::]'  # [::] is allow all host


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
        write_func = sys.stdout.write
        write_func("\n")
        write_func("---------------------\n")
        write_func('Hits:\n')
        for page_name in cls.page_count.keys():
            write_func('%s: %d\n' % (page_name, cls.page_count[page_name]))
        write_func("---------------------\n")

        sys.stdout.flush()

    def Increment(self, request, _):
        Counter.total_count += 1
        try:
            Counter.page_count[request.name] += 1
        except KeyError:
            Counter.page_count[request.name] = 1

        self.print_data()

        return counter_pb2.IncrementResponse(count=Counter.page_count[request.name])


def run_server(bind_addr):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    counter_pb2_grpc.add_CounterServicer_to_server(Counter(), server)
    server.add_insecure_port(bind_addr)
    server.start()
    print("Counter Server Start!!!")

    try:
        while True:
            sleep(__ONE_DAY_BY_SECOND)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run_server()
