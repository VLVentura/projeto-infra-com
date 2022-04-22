#!/usr/bin/env python3
from rdt import rdt

class Manipulation(rdt):
    def __init__(self, rcvpkt) -> None:
        self.rcvpkt = rcvpkt
        pass

    def extract(self, rcvpkt :bytes, data :str):
        return self.rcvpkt.decode().split("\x01")

    def deliver_data(self, data :str):
        pass

