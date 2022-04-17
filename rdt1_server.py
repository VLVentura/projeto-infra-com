#!/usr/bin/env python3
import udp_imports as udp
def extract(pkt :bytes)->str:
    return pkt.decode()
def deliver_data(data :str, client_add):
    print(f"This was yous message from {client_add}: {data}")
    udp.CONN.sendto(data.encode(),client_add)
    return
if __name__ == "__main__":
    rdt_server_loop()
