#!/usr/bin/env python3
from rdt import rdt
from packet import Packet
from socket import socket, AF_INET, SOCK_DGRAM

class Transfer(rdt):
    def make_socket(self):
        return socket(AF_INET, SOCK_DGRAM)

    def __init__(self, data, src_port, dest_port,server_name="localhost",length=32,seg_num=0 ,checksum=00000000000):
        self.data = data
        self.connection = Transfer.make_socket(self)
        self.segment = Packet()
        self.server_name = server_name
        self.segment.set_header(length, seg_num, src_port, dest_port, checksum)
        return

    def send(self,data):
        #compute checksum here
        self.segment.make_pkt(self.segment.segnum, data, checksum)
        Transfer.udt_send(self, self.segment)
        return

    def udt_send(self, sndpkt:str):
        self.connection.sendto(sndpkt.encode(), (self.server_name, self.segment.dest_port))

    def rcv(self, rcvpkt :bytes):
        return self.connection.recvfrom(2048)
        pass
