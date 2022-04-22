#!/usr/bin/env python3

from rdt import rdt


class Integrity(rdt):
    def __init__(self) -> None:
        pass

    def corrupt(self, rcvpkt :bytes):

        return

    def isACK0(self, rcvpkt :bytes, seqNum :int):
        return

    def isACK1(self, rcvpkt :bytes, segNum :int):
        return

    def timeout(self):
        return

    def start_timer(self):
        return

    def notcorrupt(self ,rcvpkt :bytes):
        return

    def stop_timer(self):
        return

    def has_seq0(self, rcvpkt :bytes):
        return

    def has_seq1(self, rcvpkt :bytes):
        return
