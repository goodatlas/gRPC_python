import argparse
from web import WebApp
from counter.server import run_server
from dns.server import run_grpc_server, run_dns_server

parser = argparse.ArgumentParser()
parser.add_argument("--counter", help="counter address and port")
parser.add_argument("--dns", help="dns address and port")
parser.add_argument("--listen_ip", help="ip address to listen")
parser.add_argument("--listen_port", help="port to listen")
parser.add_argument("--name", help="app name. can be 'dns', 'frontend', 'proxy', 'counter")


if __name__ == '__main__':
    args = parser.parse_args()
    if args.name in ['frontend', 'proxy']:
        WebApp(args.name, args.listen_ip, args.listen_port, args.counter, args.dns).run()

    elif args.name == 'dns_grpc':
        run_grpc_server()

    elif args.name == 'dns_server':
        run_dns_server(args.dns)

    elif args.name == 'counter':
        run_server()

    else:
        raise RuntimeError("Invalid App name!!")
