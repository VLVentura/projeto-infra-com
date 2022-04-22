#!/usr/bin/env python3

from rdt import rdt
import struct
import socket
from Msg_functions import Msg_functions

class Integrity(rdt):
    def __init__(self) -> None:
        pass

    def corrupt(self, rcvpkt :bytes):

        return

    def isACK0(self, rcvpkt :bytes, seqNum :int):
        (msg_type, recv_seq_num, _, _), _ = __unpack_helper(recvpkt)
        return  msg_type == 11 and recv_seq_num == seqNum       #11 é valor arbitrário, escolhido na criação do ack, representando o tipo dele

    def isACK1(self, rcvpkt :bytes, segNum :int):
        return

    def timeout(self):
        return

    def start_timer(self):
        return

    def notcorrupt(self ,rcvpkt :bytes):
        (msg_type, seq_num, recv_checksum, payload_len), payload = __unpack_helper(recvpkt)
        init_msg = struct.Struct('B?HH').pack(msg_type, seq_num, 0, socket.htons(payload_len)) + payload
        calc_checksum = checksum(bytearray(init_msg)) #precisa chamar corretamente, tá errado isso aq
        return  recv_checksum == calc_checksum  #true se não corrompido

    def stop_timer(self):
        return

   def has_seq0(self, rcvpkt :bytes, seqNum :int):
        (msg_type, recv_seq_num, _, _), _ = __unpack_helper(rcvpkt)
        return  recv_seq_num == seqNum  #true se recebe pacote do sequence number

    def has_seq1(self, rcvpkt :bytes):
        return
