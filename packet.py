#!/usr/bin/env python3

from _typeshed import Self


class Packet:
    def __init__(self) -> None:
        self.data = ""
        self.length = 0
        self.segnum = -1
        self.src_port = 0000
        self.dest_port = 0000
        self.checksum = 000000000000000
        self.segment = []
        pass

    def compose(self) -> None:
        """ Aggregate attributes in segment list"""
        self.segment.append(str(self.data))
        self.segment.append(str(self.length))
        self.segment.append(str(self.src_port))
        self.segment.append(str(self.dest_port))
        self.segment.append(str(self.checksum))

    def set_header(self ,length, seg_num ,src_port, dest_port, checksum) -> None:
        """ Set the header for this segment"""
        self.length = length
        self.src_port = src_port
        self.segnum = seg_num
        self.dest_port = dest_port
        self.checksum = checksum
        self.segment = []
        Packet.compose(self)

    def make_pkt(self, segNum:int, data :str, checksum :bytes):
        """ Create the segment"""
        self.segnum = segNum
        self.data = data
        self.checksum = checksum
        Packet.compose(self)
        return self.segment
