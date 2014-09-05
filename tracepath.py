__author__ = 'pegerto@gmail.com'

import socket
import struct
import random
import time
import argparse

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


def create_packet(id, dbytes):
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,0,id,1)
    data = dbytes * 'P'
    pkg_checksum = checksum(header+data)
    return struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(pkg_checksum), id, 1) + data


def ping(dest,dbytes):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
        packet_id = int(random.random() % 65535)
        packet = create_packet(packet_id, dbytes)

        sent = sock.sendto(packet, (dest, 1))
        sent_time = time.time()
        rec_packet, addr = sock.recvfrom(1024)
        recv_time = time.time()

        print recv_time - sent_time

    except socket.error as e:
        print "ERROR: " + e.strerror

    except Exception as e:
        print "ERROR: " + e.message


def main():
    parser = argparse.ArgumentParser(description='Dynamically discover the PMTU of a path')
    parser.add_argument('ip',type=str, help='Destination ip')
    args = parser.parse_args()
    ping(args.ip, 40)


if __name__ == '__main__':
    main()

