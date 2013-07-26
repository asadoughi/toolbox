#!/usr/bin/env python
# Sourced from http://code.activestate.com/recipes/491264-mini-fake-dns-server/

import socket


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
            packet += str.join("", map(lambda x: chr(int(x)), ip.split(".")))
        return packet


def main():
    ip = "192.168.1.1"
    print "pyminifakeDNS:: dom.query. 60 IN A %s" % ip

    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.bind(("", 53))

    try:
        while 1:
            data, addr = udps.recvfrom(1024)
            p = DNSQuery(data)
            udps.sendto(p.response(ip), addr)
            print "Response: %s -> %s" % (p.domain, ip)
    except KeyboardInterrupt:
        print "Finalizando"
        udps.close()

if __name__ == "__main__":
    main()
