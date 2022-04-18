#!/usr/bin/env python3
import udp_imports as udp

# State: wait for call from below
def rdt_server_loop():
    udp.CONN.bind(("",udp.SERVER_PORT))
    print(f"Server is listening on port: {udp.SERVER_PORT}")
    while True:
        rcvpkt_data, client_address = udp.CONN.recvfrom(2048)
        print(f"Connection stablished with {client_address}")
        sndpkt = rdt_rcv(rcvpkt_data)
        sndpkt.dest_port = client_address[1]
        udp.udt_send(sndpkt)
def send_NACK(cl_address, seq :int):
    sndpkt = udp.Packet("0",4,udp.SERVER_PORT,udp.SERVER_PORT,seq,"")
    sndpkt.dest_port = cl_address[1]
    chksum = udp.compute_chksum(sndpkt)
    udp.udt_send(udp.make_pkt(sndpkt, chksum))

def send_ACK(cl_address, seq :int):
    sndpkt = udp.Packet("1",4,udp.SERVER_PORT,udp.SERVER_PORT,seq,"")
    sndpkt.dest_port = cl_address[1]
    chksum = udp.compute_chksum(sndpkt)
    udp.udt_send(udp.make_pkt(sndpkt, chksum))

def dataIntegrity(data: bytes)->bool:
   sent_message, message_checksum = udp.parse_package(data)
   return message_checksum == udp.checksum([sent_message])

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

def deliver_data(data :str):
    print(f"MESSAGE RECEIVED {data}")

if __name__ == "__main__":
    rdt_server_loop()
