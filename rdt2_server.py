#!/usr/bin/env python3
import udp_imports as udp

# State: wait for call from below
def rdt_server_loop():
    udp.CONN.bind(("",udp.SERVER_PORT))
    print(f"Server is listening on port: {udp.SERVER_PORT}")
    while True:
        pkt, client_address = udp.CONN.recvfrom(2048)
        print(f"Connection stablished with {client_address}")
        rdt_rcv(pkt,client_address);


def rdt_rcv(rcvpkt_data :bytes)->udp.Packet:
    rcvpkt_status = dataIntegrity(rcvpkt_data)
    sndpkt = udp.Packet("null",udp.SERVER_PORT,udp.CLIENT_PORT,"00000000")
    if rcvpkt_status is True:
        deliver_data(extract(rcvpkt_data))
        sndpkt = udp.make_pkt(sndpkt,"1",udp.checksum(["1"]))
        # We assum an ACK
    else:
        sndpkt = udp.make_pkt(sndpkt,"0",udp.checksum(["0"]))
        # We assume a NACK
    return sndpkt

def extract(pkt :bytes)->str:
    return pkt.decode()

def deliver_data(data :str, client_add):
    print(f"This was yous message from {client_add}: {data}")
    udp.CONN.sendto(data.encode(),client_add)

if __name__ == "__main__":
    rdt_server_loop()
