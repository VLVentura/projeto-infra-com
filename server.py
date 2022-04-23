#!/usr/bin/env python3
from manipulation import Manipulation
from integrity import Integrity
from transfer import Transfer
SERVER_PORT = 12000
SERVER_NAME = "localhost"
def server_wait_for_0_from_below(server):
    rcvpkt, address = Transfer.rcv(server)
    newIntegrityCheck = Integrity()
    newManipulation = Manipulation(rcvpkt)
    while True:
        if(Integrity.corrupt(newIntegrityCheck,rcvpkt) and
        Integrity.has_seq1(newIntegrityCheck,rcvpkt)):
            Transfer.set_segnum(server, 1)
            Transfer.send(server,"ACK")
            Transfer.set_add(server, address)
            rcvpkt, address = Transfer.rcv(server)

        elif(Integrity.notcorrupt(newIntegrityCheck,rcvpkt) and
            Integrity.has_seq0(newIntegrityCheck,rcvpkt)):
            newManipulation.extract()
            newManipulation.deliver_data()
            Transfer.set_segnum(server, 0)
            Transfer.send(server, "ACK")
            server_wait_for_1_from_below(server)
def server_wait_for_1_from_below(server):
    rcvpkt, address = Transfer.rcv(server)
    newIntegrityCheck = Integrity()
    newManipulation = Manipulation(rcvpkt)
    while True:
        if(Integrity.corrupt(newIntegrityCheck,rcvpkt) and
        Integrity.has_seq0(newIntegrityCheck,rcvpkt)):
            Transfer.set_segnum(server, 0)
            Transfer.send(server,"ACK")
            Transfer.set_add(server, address)
            rcvpkt, address = Transfer.rcv(server)

        elif(Integrity.notcorrupt(newIntegrityCheck,rcvpkt) and
            Integrity.has_seq1(newIntegrityCheck,rcvpkt)):
            newManipulation.extract()
            newManipulation.deliver_data()
            Transfer.set_segnum(server, 1)
            Transfer.send(server, "ACK")
            server_wait_for_0_from_below(server)
