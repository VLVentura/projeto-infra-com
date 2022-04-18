#!/usr/bin/env python3
import udp_imports as udp

def make_pkt(sndpkt :udp.Packet,data :str, checksum :str)->udp.Packet:
    sndpkt.data = (data + "\x01" + checksum).encode()
    return sndpkt
def udt_send(sndpkt :udp.Packet):
    udp.CONN.sendto(sndpkt.data, (udp.SERVER_HOST,sndpkt.dest_port))
def isNACK(rcvpkt_data :bytes) -> bool:
    return udp.parse_package(rcvpkt_data) == "0"

def isACK(rcvpkt_data :bytes) -> bool:
    return udp.parse_package(rcvpkt_data) == "1"
# State wait for call from above
def rdt_send(data :str):
    newpkt = udp.Packet("null", udp.CLIENT_PORT,udp.SERVER_PORT, "00000000")
    checksum = udp.checksum([data])

    udt_send(make_pkt(newpkt, data,checksum))

def udt_send(pkt :udp.Packet):
    udp.CONN.sendto(pkt.data, (udp.SERVER_NAME,udp.SERVER_PORT))

if __name__ == "__main__":
    rdt_send(input("MESSAGE: "))
