from webapp import WebApp
from socket import *


class Frontend(WebApp):
    def bind(self, bind_addr, backlog=5):
        self.s.bind(bind_addr)
        self.s.listen(backlog)

    def __init__(self, bind_addr, upstream_addr):
        super().__init__()

        # Set Attr
        # --------

        # Setting Socket for web request
        self.s = socket(AF_INET, SOCK_STREAM)
        self.bind(bind_addr)

        # Setting grpc request channel
        self.__set_channel_stub(upstream_addr)

    def start(self):
        while True:
            client, addr = self.s.accept()
            client.recv(1024)

            count = self.__increase_count()

            client.send(b"""
            Name: %s
            Count: %d
            """ % (self.name, count))

            client.close()

