from functools import reduce
import sys
class Checksum:
    @staticmethod
    def calc(data: list[bytearray])->bytes:
        num_arr = [(int.from_bytes(data[x],byteorder=sys.byteorder)) for x in range(len(data))]
        byte = bin(reduce(Checksum.__sum_bytes,num_arr))
        final_byte = reduce(Checksum.inv,byte[2]).encode('utf-8')
        return final_byte


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
