from socket import socket, AF_INET, SOCK_DGRAM

from checksum import Checksum
from packet import Packet


class Rdt:
    def __init__(self, address: str = None, port: int = None, server_info: "tuple[str, str]" = None, timeout: int = 10):
        self.__conn = socket(AF_INET, SOCK_DGRAM)
        bind_info = (address, port)
        if server_info is not None:
            self.__server_info = server_info
            self.__conn.settimeout(timeout)
            bind_info = ("", 0)
        self.__conn.bind(bind_info)

    @staticmethod
    def create_server_connection(address: str, port: int) -> "Rdt":
        rdt = Rdt(address=address, port=port)
        return rdt

    @staticmethod
    def create_client_connection(server_address: str, server_port: int, timeout: int = 10) -> "Rdt":
        rdt = Rdt(server_info=(server_address, server_port), timeout=timeout)
        return rdt

    def send(self, data: str, addr: "tuple[str, str]" = None):
        # chksum = Checksum.calc(data)
        addr = addr if addr is not None else self.__server_info
        sndpkt = Packet()
        sndpkt.payload = data
        self.__udt_send(sndpkt.serialize(), addr)

    def recv(self) -> "tuple[str, tuple[str, str]]":
        rcvpkt, addr = self.__conn.recvfrom(2048)
        packet = Packet()
        packet.parse_from_bytes(rcvpkt)
        return (packet.payload, addr)

    def __udt_send(self, sndpkt: bytes, addr: "tuple[str, str]"):
        self.__conn.sendto(sndpkt, addr)

    # interface for integrity class
    def __corrupt(self, rcvpkt: bytes):
        """Check if segment received is corrupted"""
        pass

    def __is_ack0(self, rcvpkt: bytes, seqNum: int):
        """Check if segment has ACK as data value"""
        pass

    def __not_corrupt(self, rcvpkt: bytes):
        """Check if the segment received has not been corrupted"""
        pass

    def __has_seq0(self, rcvpkt: bytes):
        """Check if segment has sequence number 0"""
        pass

    def __has_seq1(self, rcvpkt: bytes):
        """Check if segment has sequence number 1"""
        pass
