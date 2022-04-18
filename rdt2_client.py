#!/usr/bin/env python3
import udp_imports as udp

def make_pkt(sndpkt :udp.Packet,data :str, checksum :str)->udp.Packet:
    sndpkt.data = (data + "\x01" + checksum).encode()
    return sndpkt
# State wait for call from above
def rdt_send(data :str):
    pkt = udp.Packet("null", udp.CLIENT_PORT,udp.SERVER_PORT)
    udt_send(make_pkt(pkt, data.encode()))
    msg_rcv, server_address = udp.CONN.recvfrom(2048)
    print(f"This was sent by {server_address}: {msg_rcv}")
    udp.CONN.close()

def make_pkt(pkt :udp.Packet,data :bytes)->udp.Packet:
    pkt.data = data
    return pkt

def udt_send(pkt :udp.Packet):
    udp.CONN.sendto(pkt.data, (udp.SERVER_NAME,udp.SERVER_PORT))

if __name__ == "__main__":
    rdt_send(input("MESSAGE: "))
