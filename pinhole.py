#!/usr/bin/env python
# Sourced from http://code.activestate.com/recipes/114642-pinhole/

import sys
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

BUFFER_SIZE = 1024
LISTEN_QUEUE = 5


class PipeThread(Thread):
    pipes = []

    def __init__(self, source, sink):
        Thread.__init__(self)
        self.source = source
        self.sink = sink
        PipeThread.pipes.append(self)

    def run(self):
        data = True
        while data:
            data = self.source.recv(BUFFER_SIZE)
            print "[%s => %s]: (%s)\n" % (self.source.getsockname(),
                                          self.sink.getsockname(), data)
            if data:
                self.sink.send(data)

        PipeThread.pipes.remove(self)


class Pinhole(Thread):
    def __init__(self, port, newhost, newport):
        Thread.__init__(self)
        self.newhost = newhost
        self.newport = newport
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(('', port))
        self.sock.listen(LISTEN_QUEUE)

    def run(self):
        while True:
            newsock, address = self.sock.accept()
            fwd = socket(AF_INET, SOCK_STREAM)
            fwd.connect((self.newhost, self.newport))
            PipeThread(newsock, fwd).start()
            PipeThread(fwd, newsock).start()


def main():
    if len(sys.argv) == 4:
        port = int(sys.argv[1])
        newhost = sys.argv[2]
        newport = int(sys.argv[3])
        Pinhole(port, newhost, newport).start()
    else:
        print >>sys.stderr, sys.argv[0], "<port> <src_host> <src_port>"


if __name__ == '__main__':
    main()
