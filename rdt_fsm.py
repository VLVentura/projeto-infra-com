from checksum import Checksum
from packet import Packet


class RdtFSM:
    @staticmethod
    def r0(packet: "Packet", seq_num: int) -> bool:
        return RdtFSM.not_corrupt(packet) and (RdtFSM.__has_seq0(packet) and seq_num == packet.seq_num)

    @staticmethod
    def r1(packet: "Packet", seq_num: int) -> bool:
        return RdtFSM.is_corrupt(packet) or (RdtFSM.__has_seq0(packet) and seq_num != packet.seq_num)

    @staticmethod
    def r2(packet: "Packet", seq_num: int) -> bool:
        return RdtFSM.not_corrupt(packet) and (RdtFSM.__has_seq1(packet) and seq_num == packet.seq_num)

    @staticmethod
    def r3(packet: "Packet", seq_num: int) -> bool:
        return RdtFSM.is_corrupt(packet) or (RdtFSM.__has_seq1(packet) and seq_num != packet.seq_num)

    @staticmethod
    def is_corrupt(packet: "Packet") -> bool:
        # TODO: (FIX) - Checksum
        # return packet.checksum != Checksum.calc(packet.payload)
        return False

    @staticmethod
    def is_ack(packet: "Packet") -> bool:
        return packet.payload == Packet.ACK

    @staticmethod
    def not_corrupt(packet: "Packet") -> bool:
        return not RdtFSM.is_corrupt(packet)

    @staticmethod
    def __has_seq0(packet: "Packet") -> bool:
        return packet.seq_num == 0

    @staticmethod
    def __has_seq1(packet: "Packet") -> bool:
        return packet.seq_num == 1
