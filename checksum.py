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
    def __sum_bytes(acc:int,act:int):
        return acc + act

    @staticmethod
    def inv(acc:str, act:str):
        if act == '1':
            acc =  acc + '0'
        elif act == '0':
            acc = acc + '1'
        return acc
