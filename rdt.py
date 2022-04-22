from copy import deepcopy
import json
from socket import socket, timeout


class Rdt:
    ACK = "ACK"

    def __init__(self, conn: socket):
        self.__packet = self.__read_json("packet.json")
        self.__conn = conn
        self.__recv_seq = 0
        self.__send_seq = 0

    def send(self, dst_info: "tuple[str, str]", message: str):
        packet = self.__make_packet(message, self.__send_seq, dst_info[1])
        packet_encoded = json.dumps(packet).encode()
        self.__conn.sendto(packet_encoded, dst_info)

        self.__wait_for_ack(packet_encoded, dst_info)
        self.__send_seq = 0 if self.__send_seq == 1 else 1

    def recv(self) -> "tuple[str, tuple[str, int]]":
        run = True
        data, src_info = None, None

        while run:
            packet, src_info = self.__conn.recvfrom(2048)
            packet_decoded = json.loads(packet.decode("utf-8"))
            num_seq = -1

            if self.__recv_r0(packet_decoded, packet_decoded["header"]["num_seq"]):
                run = False
                data = packet_decoded["payload"]
                num_seq = 0
            elif self.__recv_r1(packet_decoded, packet_decoded["header"]["num_seq"]):
                num_seq = 0
            elif self.__recv_r2(packet_decoded, packet_decoded["header"]["num_seq"]):
                run = False
                data = packet_decoded["payload"]
                num_seq = 1
            elif self.__recv_r3(packet_decoded, packet_decoded["header"]["num_seq"]):
                num_seq = 1

            packet = self.__make_packet(self.ACK, num_seq, src_info[1])
            self.__conn.sendto(json.dumps(packet).encode(), src_info)
            if run is False:
                self.__recv_seq = 0 if self.__recv_seq == 1 else 1

        return (data, src_info)

    def __make_packet(self, message: str, num_seq: int, dst_port: int) -> dict:
        packet = deepcopy(self.__packet)
        packet["header"]["num_seq"] = num_seq
        packet["header"]["checksum"] = self.__checksum([message])
        packet["header"]["src_port"] = self.__conn.getsockname()[1]
        packet["header"]["dst_port"] = dst_port
        packet["header"]["len"] = len(message)
        packet["payload"] = message
        return packet

    def __is_ack(self, packet: dict) -> bool:
        return packet["payload"] == self.ACK

    def __is_corrupted(self, packet: dict) -> bool:
        return packet["header"]["checksum"] != self.__checksum([packet["payload"]])

    def __has_seq0(self, packet: dict) -> bool:
        return packet["header"]["num_seq"] == 0

    def __has_seq1(self, packet: dict) -> bool:
        return packet["header"]["num_seq"] == 1

    def __recv_r0(self, packet: dict, num_seq: int) -> bool:
        return not self.__is_corrupted(packet) and (self.__has_seq0(packet) and num_seq == self.__recv_seq)

    def __recv_r1(self, packet: dict, num_seq: int) -> bool:
        return self.__is_corrupted(packet) or (self.__has_seq0(packet) and num_seq != self.__recv_seq)

    def __recv_r2(self, packet: dict, num_seq: int) -> bool:
        return not self.__is_corrupted(packet) and (self.__has_seq1(packet) and num_seq == self.__recv_seq)

    def __recv_r3(self, packet: dict, num_seq: int) -> bool:
        return self.__is_corrupted(packet) and (self.__has_seq1(packet) and num_seq != self.__recv_seq)

    def __wait_for_ack(self, orig_packet: str, dst_info: "tuple[str, str]"):
        run = True

        while run:
            try:
                packet, _ = self.__conn.recvfrom(2048)
                pkt_decoded = json.loads(packet.decode("utf-8"))
                num_seq = pkt_decoded["header"]["num_seq"]

                if not self.__is_corrupted(pkt_decoded) and (self.__is_ack(pkt_decoded) and num_seq == self.__send_seq):
                    run = False
            except timeout:
                print("Socket timeout, trying to send the message again.")
            finally:
                self.__conn.sendto(orig_packet, dst_info)

    def __str_to_binary(self, messages: list) -> list:
        binary_messages = []
        for message in messages:
            binary_messages.append("".join(format(i, "08b") for i in bytearray(message, encoding="utf-8")))
        return binary_messages

    def __checksum(self, message: list) -> str:
        var = self.__str_to_binary(message)
        var2 = [ord("0") for _ in range(len(var[0]))]

        for i in range(len(var)):
            for j in range(len(var[i])):
                var2[j] += ord(var[i][j])

        for i in range(len(var2)):
            if i < len(var2):
                resto = var2[i] % 48
                if resto == 0:
                    var2[i] = ord("0")
                if resto == 1:
                    var2[i] = ord("1")
                if resto == 2:
                    var2[i] = ord("1")
                    var2[(i + 1)] += ord("1")

            if i == len(var2):
                resto = var2[i] % 48
                if resto == 0:
                    var2[i] = ord("0")
                if resto == 1:
                    var2[i] = ord("1")
                if resto == 2:
                    var2[i] = ord("1")
                    var2[0] += ord("1")

        for i in range(len(var2)):
            if i < len(var2):
                resto = var2[i] % 48
                if resto == 0:
                    var2[i] = ord("0")
                if resto == 1:
                    var2[i] = ord("1")
                if resto == 2:
                    var2[i] = ord("1")
                    var2[(i + 1)] += ord("1")

            if i == len(var2):
                resto = var2[i] % 48
                if resto == 0:
                    var2[i] = ord("0")
                if resto == 1:
                    var2[i] = ord("1")
                if resto == 2:
                    var2[i] = ord("1")
                    var2[0] += ord("1")

        for i in range(len(var2)):
            var2[i] = var2[i] // ord("1")

        for i in range(len(var2)):
            if var2[i] == 0:
                var2[i] = 1
            else:
                var2[i] = 0

        return "".join([str(x) for x in var2])

    def __read_json(self, filename: str) -> dict:
        packet = None
        with open(filename) as file:
            packet = json.load(file)
        return packet
