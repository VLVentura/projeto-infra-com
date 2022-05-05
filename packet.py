import json


class Packet:
    def __init__(
        self,
        seq_num: int = 0,
        checksum: bytearray = bytearray(15),
        src_port: int = 0,
        dest_port: int = 0,
        length: int = 25,
        payload: str = "",
    ):
        self.__packet = {
            "header": {
                "seq_num": seq_num,
                "checksum": bytes(checksum).decode("utf-8"),
                "src_port": src_port,
                "dest_port": dest_port,
                "length": length,
            },
            "payload": payload,
        }

    def __str__(self):
        return json.dumps(self.__packet, indent=4)

    @property
    def seq_num(self) -> int:
        return self.__packet["header"]["seq_num"]

    @seq_num.setter
    def seq_num(self, seq_num: int):
        self.__packet["header"]["seq_num"] = seq_num

    @property
    def checksum(self) -> bytearray:
        return bytearray(self.__packet["header"]["checksum"].encode("utf-8"))

    @checksum.setter
    def checksum(self, checksum: bytearray(15)):
        self.__packet["header"]["checksum"] = bytes(checksum).decode("utf-8")

    @property
    def src_port(self) -> int:
        return self.__packet["header"]["src_port"]

    @src_port.setter
    def src_port(self, src_port: int):
        self.__packet["header"]["src_port"] = src_port

    @property
    def dest_port(self) -> int:
        return self.__packet["header"]["dest_port"]

    @dest_port.setter
    def dest_port(self, dest_port: int):
        self.__packet["header"]["dest_port"] = dest_port

    @property
    def length(self) -> int:
        return self.__packet["header"]["length"]

    @length.setter
    def length(self, length: int):
        self.__packet["header"]["length"] = length

    @property
    def payload(self) -> str:
        return self.__packet["payload"]

    @payload.setter
    def payload(self, payload: str):
        self.__packet["payload"] = payload

    def set_header(self, seq_num: int, checksum: bytearray(15), src_port: int, dest_port: int, length: int) -> None:
        self.__packet["header"]["seq_num"] = seq_num
        self.__packet["header"]["checksum"] = bytes(checksum).decode("utf-8")
        self.__packet["header"]["src_port"] = src_port
        self.__packet["header"]["dest_port"] = dest_port
        self.__packet["header"]["length"] = length

    def set_payload(self, payload: str) -> None:
        self.__packet["payload"] = payload

    def serialize(self) -> bytes:
        return json.dumps(self.__packet).encode("utf-8")

    def parse_from_bytes(self, rcvpkt: bytes) -> None:
        self.__packet = json.loads(rcvpkt)
