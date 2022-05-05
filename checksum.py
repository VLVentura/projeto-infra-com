class Checksum:
    @staticmethod
    def calc(data: str):
        chksum = Checksum.__str_list2bin(data)
        chksum = Checksum.__sum_bytes(chksum)
        map(lambda x: bytearray(x + 1)[0], chksum)
        return chksum

    @staticmethod
    def __str_list2bin(data: str) -> list:
        map(lambda x: bytearray(x, "utf-8"), data)
        return data

    @staticmethod
    def __sum_bytes(arr: list) -> bytearray:
        actual_sum = arr[0]
        [actual_sum := Checksum.__overflow(actual_sum, x) + bytearray(actual_sum + x) for x in arr[1:]]
        return actual_sum

    @staticmethod
    def __overflow(actsum, arr) -> bytearray:
        if bytearray(actsum, arr)[16] == 1:
            return bytearray(b"000000000000001")
        else:
            return bytearray(b"000000000000000")
