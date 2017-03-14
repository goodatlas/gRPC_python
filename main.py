import argparse
from frontend import Frontend
from proxy import Proxy
from counter.server import run_server


parser = argparse.ArgumentParser()
# parser.add_argument("--counter", help="counter address and port")
# parser.add_argument("--dns", help="dns address and port")
# parser.add_argument("--listen_ip", help="ip address to listen")
# parser.add_argument("--listen_port", help="port to listen")
parser.add_argument("--upstream", help="upstream addr and port")
parser.add_argument("--bind", help="bind addr and port")
parser.add_argument("--name", help="app name. can be 'dns', 'frontend', 'proxy', 'counter")
parser.add_argument("--dnslb", help="use client load balancer", action='store_true', default=False)

def channel_options(args):
    return [('grpc.lb_policy_name', 'round_robin')] if args.dnslb else None

if __name__ == '__main__':
    args = parser.parse_args()
    name = args.name

    if name == 'frontend':
        f = Frontend(name, args.upstream, args.bind, channel_options(args))
        f.start()

    elif name == 'proxy':
        p = Proxy(name, args.upstream, args.bind, channel_options(args))
        p.start()

    elif name == 'counter':
        run_server()

    else:
        raise RuntimeError("Invalid App name!!")
