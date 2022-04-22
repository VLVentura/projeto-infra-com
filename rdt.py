#!/usr/bin/env python3

class rdt:

    # interface for transfer class
    def send(self,data: str):
        """ Start the routine to send a segment"""
        pass

    def udt_send(self, sndpkt : bytes):
        """  Send segmentthrough UDP"""
        pass

    def rcv(self, rcvpkt :bytes):
        """ Receive segment"""
        pass

    #interface for integrity class

    def corrupt(self, rcvpkt :bytes)-> bool:
        """ Check if segment received is corrupted"""
        pass

    def isACK(self, rcvpkt :bytes, seqNum :int) -> bool:
        """ Check if segment has ACK as data value"""
        pass

    def timeout(self) -> bool:
        """ Check if the actual timer has excedeed"""
        pass

    def start_timer(self):
        """ Start a timer"""
        pass

    def notcorrupt(self ,rcvpkt :bytes) -> bool:
        """ Check if the segment received has not been corrupted"""
        pass

    def stop_timer(self):
        """ Actual timer has been stopped"""
        pass

    def has_seq0(self, rcvpkt :bytes) -> bool:
        """ Check if segment has sequence number 0"""
        pass

    def has_seq1(self, rcvpkt :bytes) -> bool:
        """ Check if segment has sequence number 1"""
        pass

    #interface for manipulation class
    def extract(self, rcvpkt :bytes, data :str):
        """ Extract segment data"""
        pass

    def deliver_data(self, data :str):
        """ Send data to the application layer"""
        pass
