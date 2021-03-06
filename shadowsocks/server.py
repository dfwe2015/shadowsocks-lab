#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import json
import os
import sys
import logging

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)
from shadowsocks.eventloop import EventLoop
from shadowsocks.tcprelay import TcpRelay, TcpRelayServerHandler
from shadowsocks.asyncdns import DNSResolver


FORMATTER = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def main():
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
    config = json.load(open(config_file))
    listen_addr = (config['server'], config['server_port'])
    method = config['method']
    password = config['password']
    log_level = config.get('log-level', 'INFO').upper()
    log_file = config.get('log-file')
    logging.basicConfig(level=getattr(logging, log_level), format=FORMATTER,
                        filename=log_file)

    loop = EventLoop()
    dns_resolver = DNSResolver()
    relay = TcpRelay(TcpRelayServerHandler, listen_addr, method, password,
                     dns_resolver=dns_resolver)
    dns_resolver.add_to_loop(loop)
    relay.add_to_loop(loop)
    loop.run()

if __name__ == '__main__':
    main()
