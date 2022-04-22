#!/usr/bin/env python3
class Packet:
    def __init__(self, data,lenght, src_port, dest_port, seq,checksum):
        self.data = data
        self.seq = seq
        self.length = lenght
        self.src_port = src_port
        self.dest_port = dest_port
        self.checksum = checksum

