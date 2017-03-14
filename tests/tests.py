# -*- coding: utf-8 -*-
import unittest


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()

    # Things TODO
    # - GRPC Test
    # -- from Proxy, to Counter
    # -- from Frontend, to Proxy
    # - Web Request Test
    # -- from client, to Frontend with HTTP
