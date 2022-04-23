#!/usr/bin/env python3
from packet import Packet
import copy

class Checksum:
        def __init__(self, segment :Packet, target=bytearray(15)):
            self.segment = segment
            self.target = target
            self.binArr = []

        def calc_checksum(self):
            Checksum.str_list2bin(self)
            map(lambda x: bytearray(x + b'1'), self.segment.segment)
            return self.segment.segment

        def str_list2bin(self):
            new_segment = copy.deepcopy(self.segment)
            map(lambda x: bytearray(x, 'utf-8'), new_segment.segment) #HACK this is very hacky
            self.segment = new_segment
            pass

        @staticmethod
        def overflow(actsum, arr)->bytearray:
                if bytearray(actsum, arr)[16] == 1:
                        return bytearray(b'000000000000001')
                else:
                        return bytearray(b'000000000000000')

        def sum_bytes(self)->bytearray:
            actual_sum = self.segment;
            [actual_sum := Checksum.overflow(actual_sum, x) + bytearray(actual_sum + x )for x in self.segment.segment[1:]]
            return actual_sum

        @staticmethod
        def verify_bytes(pkt,target)->bool:
                pkt
