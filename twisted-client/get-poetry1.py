#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan
import optparse

import sys
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory, connectionDone


def parse_args():
    usage = """usage: %prog [options] [hostname]:port ...

This is the Get Poetry Now! client, Twisted version 2.0.
Run it like this:

  python get-poetry.py port1 port2 port3 ...

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python twisted-client-2/get-poetry.py 10001 10002 10003

to grab poetry from servers on ports 10001, 10002, and 10003.

Of course, there need to be servers listening on those ports
for that to work.
"""

    parser = optparse.OptionParser(usage)

    _, addresses = parser.parse_args()

    if not addresses:
        print parser.format_help()
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr
        else:
            host, port = addr.split(':', 1)

        if not port.isdigit():
            parser.error('Ports must be integers.')

        return host, int(port)

    return map(parse_address, addresses)


class PoetryProtocol(Protocol):
    poem = ''

    def dataReceived(self, data):
        self.poem += data

    def connectionLost(self, reason=connectionDone):
        self.poemReceived(self.poem)

    def poemReceived(self, poem):
        self.factory.poem_finished(poem)


class PoetryClientFactory(ClientFactory):
    protocol = PoetryProtocol

    def __init__(self, callback, errback):
        self.callback = callback
        self.errback = errback

    def poem_finished(self, poem):
        self.callback(poem)

    def clientConnectionFailed(self, connector, reason):
        self.errback(reason)


def get_poetry(host, port, callback, errback):
    factory = PoetryClientFactory(callback, errback)
    reactor.connectTCP(host, port, factory)


def poetry_main():
    addresses = parse_args()
    poems = []
    errors = []

    def get_poem(poem):
        poems.append(poem)
        poem_done()

    def poem_failed(err):
        print >> sys.stderr, 'Poem failed', err
        errors.append(err)
        poem_done()

    def poem_done():
        if len(poems) + len(errors) == len(addresses):
            reactor.stop()

    for host, port in addresses:
        get_poetry(host, port, get_poem, poem_failed)

    reactor.run()
    for poem in poems:
        print poem


if __name__ == '__main__':
    poetry_main()
