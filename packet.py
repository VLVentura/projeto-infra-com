#!/usr/bin/env python3
class Packet:
    def __init__(self, data, src_port, dest_port):
        self.data = data
        self.src_port = src_port
        self.dest_port = dest_port
