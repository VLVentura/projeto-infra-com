#!/usr/bin/env python3

from manipulation import Manipulation
from rdt import rdt
from checksum import Checksum
   
class Integrity(rdt):
    def __init__(self) -> None:
        pass

    def corrupt(self, rcvpkt :bytes):
        return Checksum.sum_bytes(rcvpkt) != rcvpkt[0:15] # position of chekcsum in the segment

    def isACK0(self, rcvpkt :bytes, seqNum :int):
        extracted_data = Manipulation.extract(rcvpkt)
        return (extracted_data[0:-2] == 'ACK' and seqNum == 0)

    def isACK1(self, rcvpkt :bytes, seqNum :int):
        extracted_data = Manipulation.extract(rcvpkt) # return data and seqnum
        return (extracted_data[0:-2] == 'ACK' and seqNum == 1)

    def notcorrupt(self ,rcvpkt :bytes):
        return Checksum.sum_bytes(rcvpkt) == rcvpkt[0:15]

    def has_seq0(self, rcvpkt :bytes):
        extracted_data = Manipulation.extract(rcvpkt)
        return extracted_data[-1] == 0

    def has_seq1(self, rcvpkt :bytes):
        extracted_data = Manipulation.extract(rcvpkt)
        return extracted_data[-1] == 1
