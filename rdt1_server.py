#!/usr/bin/env python3
import udp_imports as udp
def rdt_rcv(pkt :bytes,client_add):
    deliver_data(extract(pkt),client_add)
    return
def extract(pkt :bytes)->str:
    return pkt.decode()
def deliver_data(data :str, client_add):
    print(f"This was yous message from {client_add}: {data}")
    udp.CONN.sendto(data.encode(),client_add)
    return
if __name__ == "__main__":
    rdt_server_loop()
