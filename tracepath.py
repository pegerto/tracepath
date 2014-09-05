__author__ = 'pegerto@gmail.com'

import socket
import struct

ICMP_ECHO_REQUEST = 8
ICMP_CODE = socket .getprotobyname('icmp')


def checksum(package):
   return 0


def create_packet(id):
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,0,id,1)
    data = 192 * 'Q'
    pkg_checksum = checksum(header+data)

    return struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(pkg_checksum), id, 1) + data

