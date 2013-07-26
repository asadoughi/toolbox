#!/usr/bin/env python
# Sourced from http://code.activestate.com/recipes/491264-mini-fake-dns-server/

from datetime import datetime
import socket


def int_to_net(ip):
    ret = ""
    for i in range(4):
        ret = chr(int(ip & 0xff)) + ret
        ip >>= 8
    return ret


class DNSQuery(object):
    def __init__(self, data):
        self.data = data
        self.domain = ""

        opcode = (ord(data[2]) >> 3) & 15

        # Standard query
        if opcode == 0:
            i = 12
            lon = ord(data[i])
            while lon:
                self.domain += data[i+1:i+lon+1] + "."
                i += lon+1
                lon = ord(data[i])

    def response(self, ip):
        packet = ""
        if self.domain:
            packet += self.data[:2] + "\x81\x80"
            # Questions and Answers Counts
            packet += self.data[4:6] + self.data[4:6] + "\x00\x00\x00\x00"
            # Original Domain Name Question
            packet += self.data[12:]
            # Pointer to domain name
            packet += "\xc0\x0c"
            # Response type, ttl and resource data length -> 4 bytes
            packet += "\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04"
            # 4 bytes of IP
            packet += int_to_net(ip)
        return packet


def main():
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.bind(("", 53))

    try:
        ip = 0
        while 1:
            data, addr = udps.recvfrom(1024)
            p = DNSQuery(data)
            udps.sendto(p.response(ip), addr)
            print "[%s] %s -> %s; %s" % (datetime.now(), p.domain, ip, addr)
            ip = (ip + 1) % 0xffffffff
    except KeyboardInterrupt:
        print "Exiting..."
        udps.close()

if __name__ == "__main__":
    main()
