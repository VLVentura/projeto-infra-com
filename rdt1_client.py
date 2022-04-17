#!/usr/bin/env python3
import udp_imports as udp
def udt_send(pkt :udp.Packet):
    udp.CONN.sendto(pkt.data, (udp.SERVER_NAME,udp.SERVER_PORT))
    return
if __name__ == "__main__":
    rdt_send(input("MESSAGE: "))
