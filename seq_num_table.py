class SeqNumTable:
    def __init__(self):
        self.__table = {}

    def add_address(self, addr: "tuple[str, str]"):
        ip = addr[0]
        port = addr[1]
        self.__table[f"{ip}:{port}"] = 0

    def remove_address(self, addr: "tuple[str, str]"):
        ip = addr[0]
        port = addr[1]
        self.__table.pop(f"{ip}:{port}")

    def get_seq_num(self, addr: "tuple[str, str]") -> int:
        ip = addr[0]
        port = addr[1]
        return self.__table[f"{ip}:{port}"]

    def update_seq_num(self, addr: "tuple[str, str]"):
        ip = addr[0]
        port = addr[1]
        val = self.__table[f"{ip}:{port}"]
        val = 0 if val == 1 else 1
        self.__table[f"{ip}:{port}"] = val

    def contains(self, addr: "tuple[str, str]") -> bool:
        ip = addr[0]
        port = addr[1]
        return self.__table.get(f"{ip}:{port}") is not None
