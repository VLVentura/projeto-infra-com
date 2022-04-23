#!/usr/bin/env python3
from packet import Packet
import copy

class Checksum:
        def __init__(self, packet :Packet, target=bytearray(15)):
            self.Packet = packet
            self.chksum = []
            self.target = target
            self.binArr = []

        def calc_checksum(self):
            Checksum.str_list2bin(self)
            self.chksum = Checksum.sum_bytes(self)
            map(lambda x: bytearray(x + 1)[0], self.chksum)
            return self.chksum

        def str_list2bin(self):
            self.binArr = copy.deepcopy(self.Packet)
            map(lambda x: bytearray(x, 'utf-8'), self.binArr.segment) #HACK this is very hacky
            self.chksum = self.binArr.segment

        @staticmethod
        def overflow(actsum, arr)->bytearray:
                if bytearray(actsum, arr)[16] == 1:
                        return bytearray(b'000000000000001')
                else:
                        return bytearray(b'000000000000000')

        @staticmethod
        def sum_bytes(arr)->bytearray:
            actual_sum = arr.chksum[0];
            [actual_sum := Checksum.overflow(actual_sum, x) + bytearray(actual_sum + x)for x in arr.chksum[1:]]
            return actual_sum
