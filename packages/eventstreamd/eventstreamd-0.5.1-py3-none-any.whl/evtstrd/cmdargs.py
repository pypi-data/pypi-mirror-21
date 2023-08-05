import argparse

from evtstrd.config import *


def parse_command_line():
    parser = argparse.ArgumentParser(
        description="A simple event stream server.")
    parser.add_argument("-c", "--config-file", help="configuration file")
    parser.add_argument("-s", "--socket", help="socket file")
    parser.add_argument("--ssl-key", help="SSL key file")
    parser.add_argument("--ssl-cert", help="SSL certificate file")
    parser.add_argument("-p", "--port", help="HTTP port", type=int)
    args = parser.parse_args()
    if args.config_file is not None:
        config = read_config(args.config_file)
    else:
        config = read_default_config()
    if args.socket is not None:
        config.socket_file = args.socket
    if args.ssl_key is not None:
        config.key_file = args.ssl_key
    if args.ssl_cert is not None:
        config.cert_file = args.ssl_cert
    if args.port is not None:
        config.http_port = args.port
    return config
