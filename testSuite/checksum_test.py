#!/usr/bin/env python3
from hypothesis.core import example, given
import sys
from functools import reduce
from hypothesis.strategies._internal.core import binary, composite, from_type, lists
from newmain.checksum import Checksum
import pytest


seq_unit = from_type(bytearray).filter(lambda x: len(x) == 1)
seq_list = lists(seq_unit,min_size=3,max_size=3)
# @example(x=[bytearray(b'\x0f1'),bytearray(b'\x0f1'),bytearray(b'\x0d1')])
@given(seq_list)
def test_sum_bytes(x):
    prev_data =Checksum.calc(x)
    print(x)
    print(prev_data)
    assert prev_data == 10

# @given()
# def test_overflow(actsum, arr):
#     assert Checksum.__overflow(actsum, arr) = #TODO must return correct sum
