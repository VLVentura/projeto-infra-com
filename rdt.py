from socket import socket, AF_INET, SOCK_DGRAM, timeout

from checksum import Checksum
from packet import Packet
from rdt_fsm import RdtFSM
from seq_num_table import SeqNumTable


class Rdt:
    def __init__(self, address: str = None, port: int = None, server_info: "tuple[str, str]" = None, timeout: int = 10):
        self.__conn = socket(AF_INET, SOCK_DGRAM)
        self.__timeout = timeout
        self.__recv_seq_table = SeqNumTable()
        self.__send_seq = 0
        self.__server_info = None

        bind_info = (address, port)
        if server_info is not None:
            self.__server_info = server_info
            bind_info = ("", 0)

        self.__conn.bind(bind_info)

    @staticmethod
    def create_server_connection(address: str, port: int, timeout: int = 10) -> "Rdt":
        rdt = Rdt(address=address, port=port, timeout=timeout)
        return rdt

    @staticmethod
    def create_client_connection(server_address: str, server_port: int, timeout: int = 10) -> "Rdt":
        rdt = Rdt(server_info=(server_address, server_port), timeout=timeout)
        return rdt

    def send(self, data: str, addr: "tuple[str, str]" = None):
        # TODO: (FIX) - Checksum
        # chksum = Checksum.calc(data)
        addr = addr if addr is not None else self.__server_info
        sndpkt = Packet(seq_num=self.__send_seq)
        sndpkt.payload = data
        self.__udt_send(sndpkt.serialize(), addr)
        self.__wait_for_ack(sndpkt, addr)
        self.__send_seq = 0 if self.__send_seq == 1 else 1

    def recv(self) -> "tuple[str, tuple[str, str]]":
        run = True
        packet = Packet()
        data, addr = None, None

        while run:
            rcvpkt, addr = self.__conn.recvfrom(2048)
            if not self.__recv_seq_table.contains(addr):
                self.__recv_seq_table.add_address(addr)

            packet.parse_from_bytes(rcvpkt)
            seq_num = -1

            if RdtFSM.r0(packet, self.__recv_seq_table.get_seq_num(addr)):
                run = False
                data = packet.payload
                seq_num = 0
            elif RdtFSM.r1(packet, self.__recv_seq_table.get_seq_num(addr)):
                seq_num = 0
            elif RdtFSM.r2(packet, self.__recv_seq_table.get_seq_num(addr)):
                run = False
                data = packet.payload
                seq_num = 1
            elif RdtFSM.r3(packet, self.__recv_seq_table.get_seq_num(addr)):
                seq_num = 1

            packet = Packet.make_ack(seq_num, self.__conn.getsockname()[1], addr[1])
            self.__udt_send(packet.serialize(), addr)
            if run is False:
                self.__recv_seq_table.update_seq_num(addr)

        return (data, addr)

    def reset_state_from(self, addr: "tuple[str, str]"):
        if self.__server_info is None:
            self.__recv_seq_table.remove_address(addr)

    def __udt_send(self, sndpkt: bytes, addr: "tuple[str, str]"):
        self.__conn.sendto(sndpkt, addr)

    def __wait_for_ack(self, orig_packet: "Packet", addr: "tuple[str, str]"):
        run = True
        packet = Packet()
        self.__start_timer()

        while run:
            try:
                bytes, _ = self.__conn.recvfrom(2048)
                packet.parse_from_bytes(bytes)
                if RdtFSM.not_corrupt(packet) and (RdtFSM.is_ack(packet) and packet.seq_num == self.__send_seq):
                    run = False

            except timeout:
                print("Socket timeout, trying to send the message again.")
                self.__udt_send(orig_packet.serialize(), addr)

        self.__reset_timer()

    def __start_timer(self):
        self.__conn.settimeout(self.__timeout)

    def __reset_timer(self):
        self.__conn.settimeout(None)
