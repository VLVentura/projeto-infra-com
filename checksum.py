#!/usr/bin/env python3
from packet import Packet

class Checksum:
        def __init__(self, segment, target=bytes(32)):
            self.segment = segment
            self.target = target

        def str_list2bin(self):
            pass

        def sum_bytes(self):
            pass

        def verify_bytes(self, target):
            pass
