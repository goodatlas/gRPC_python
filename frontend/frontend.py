from flask import Flask

from webapp import WebApp


class Frontend(WebApp):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.host, self.port = self.bind_addr.split(':')

        self.app = Flask(__name__)

    def start(self):
        @self.app.route('/count')
        def count():
            return "Name: %s\nCount: %d\n" % (self.host_name, self.increase_count().count)

        self.app.run(host=self.host, port=int(self.port))
