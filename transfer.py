#!/usr/bin/env python3
from checksum import Checksum
from rdt import rdt
from packet import Packet
from socket import socket, AF_INET, SOCK_DGRAM

class Transfer(rdt):
    def make_socket(self):
        return socket(AF_INET, SOCK_DGRAM)

    def bind_socket(self):
        return self.connection.bind((self.server_name,self.server_port))

    def __init__(self, data="", src_port=0000, dest_port=0000,server_name="localhost", server_port=12000,length=32,seg_num=0 ,checksum=00000000000):
        self.data = data
        self.connection = Transfer.make_socket(self)
        self.dest_port = dest_port
        self.segment = Packet()
        self.server_name = server_name
        self.segment.set_header(length, seg_num, src_port, dest_port, checksum)
        self.server_port = server_port
        return

    def send(self,data):
        chksum = Checksum.calc_checksum(Checksum(self.segment))
        self.segment.make_pkt(self.segment.segnum, data, chksum)
        Transfer.udt_send(self, self.segment)
        return

    def udt_send(self, sndpkt:str):
        self.connection.sendto(sndpkt.encode(), (self.server_name, self.segment.dest_port))

    def rcv(self):
        return self.connection.recvfrom(2048)

    def set_segnum(self,segnum):
        self.segment.segnum = segnum

    def set_add(self,add):
        self.dest_port = add
