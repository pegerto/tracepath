__author__ = 'pegerto@gmail.com'

import socket
import struct

ICMP_ECHO_REQUEST = 8
ICMP_CODE = socket .getprotobyname('icmp')


def checksum(package):
    suma = 0
    to = (len(package)/2) * 2
    count = 0
    while count < to:
        val = ord(package[count+1]) * 256 + ord(package[count])
        suma += val
        suma &= 0xfffffff
        count += 2
    if to < len(package):
        suma += ord(package[len(package) - 1])
        suma &= 0xfffffff
    suma = (suma >> 16) + (suma & 0xffff)
    suma += (suma >> 16)
    answer = ~suma
    answer &= 0xffff
    return (answer >> 8) | (answer << 8 & 0xff00)



def create_packet(id):
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,0,id,1)
    data = 192 * 'Q'
    pkg_checksum = checksum(header+data)
    return struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(pkg_checksum), id, 1) + data

