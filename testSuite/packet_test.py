#!/usr/bin/env python3
import hypothesis
import packet2
from hypothesis import given
from hypothesis.strategies import *
import pytest

seq_num = integers(min_value=1, max_value=2)
checksum_pre = binary(min_size=15,max_size=15).example()
src_port = integers(min_value=0, max_value = 2**16)
dest_port = integers(min_value=0, max_value = 2**16)
length = integers(min_value=64,max_value=64)
payload = from_type(str)
payload_l = lists(payload, min_size=0,max_size=None)
@given(data())
def test_serialize(pkt:packet2.Packet):
    packet2.Packet.checksum = data.draw(checksum_pre)
    packet2.Packet.src_port = data.draw(src_port)
    packet2.Packet.dest_port = data.draw(dest_port)
    packet2.Packet.length = data.draw(length)
    packet2.Packet.payload = data.draw(payload)
    assert packet2.Packet.serialize(pkt) = #TODO Make sure this is as expected and see if can figure out the header size
