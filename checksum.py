#!/usr/bin/env python3
from packet import Packet

class Checksum:
        def __init__(self, segment :Packet, target=bytearray(15)):
            self.segment = segment
            self.target = target
            self.binArr = []

        def calc_checksum(self)->bytes:
            Checksum.str_list2bin(self)
            return Checksum.sum_bytes(self)

        def str_list2bin(self):
            map(lambda x: bytearray(x, 'utf-8'), self.segment.segment) #HACK this is very hacky
            pass

        def sum_bytes(self)->bytes:
            sum_bytes = self.segment.segment[0];
            [sum_bytes := bytearray(sum_bytes + x) for x in self.segment.segment[1:]]
            return sum_bytes

        @staticmethod
        def verify_bytes(target):
            pass
