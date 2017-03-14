from webapp import WebApp


class Frontend(WebApp):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bind(self.bind_addr)

    def start(self):
        while True:
            client, addr = self.s.accept()
            client.recv(1024)

            count = self.increase_count().count

            resp = ("Name: %s\nCount: %d\n" % (self.host_name, count))

            client.send(resp.encode('utf8'))

            client.close()

