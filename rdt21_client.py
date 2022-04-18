#!/usr/bin/env python3
import udp_imports as udp

def make_pkt(pkt :udp.Packet,chksum :str)->udp.Packet:
    pkt.data = (compose(pkt) + "\x01" + chksum).encode()
    # add all attributes to data, data becomes type bytes
    return pkt

def compose(pkt: udp.Packet):
            return str(pkt.data)+str(pkt.length)+str( pkt.src_port)+str( pkt.dest_port)+str( pkt.seq )

def udt_send(sndpkt :udp.Packet):
    udp.CONN.sendto(sndpkt.data, (udp.SERVER_HOST,sndpkt.dest_port))

def isNACK(rcvpkt_data :bytes) -> bool:
    return udp.parse_package(rcvpkt_data) == "0"

def isACK(rcvpkt_data :bytes) -> bool:
    return udp.parse_package(rcvpkt_data) == "1"

# State wait for call from above
def compute_chksum(pkt :udp.Packet) -> str:
    data_to_checksum = compose(pkt)
    return udp.checksum([data_to_checksum])
def wait_for_acknoewldgemnt(rcvpkt: bytes, pkt :udp.Packet):
    while (udp.dataIntegrity(rcvpkt) or isNACK(rcvpkt)):
        print("INVALID MESSAGE RECEIVED")
        udt_send(make_pkt(pkt,pkt.checksum))
def wait_for_call(data :str, seq :int)->udp.Packet:
    pkt = udp.Packet(data, 4,udp.CLIENT_PORT,udp.SERVER_PORT,seq, "")
    chksum = compute_chksum(pkt)
    sndpkt = make_pkt(pkt, chksum)
    udt_send(sndpkt)
    return sndpkt
def rdt_send(data :str):
    #State wait for call0 from above
    sndpkt0 = wait_for_call(data, 0)
    msg_rcv0, server_address = udp.CONN.recvfrom(2048)
    print(f"This was sent by {server_address}: {udp.parse_package(msg_rcv0)[0]}")

    #State wait ACK or NAK 0
    wait_for_acknoewldgemnt(msg_rcv0,sndpkt0)

    #State wait for call1 from above
    sndpkt1 = wait_for_call(data, 1)
    msg_rcv1, server_address = udp.CONN.recvfrom(2048)
    print(f"This was sent by {server_address}: {udp.parse_package(msg_rcv1)[0]}")

    # State ACK or NAK 1
    wait_for_acknoewldgemnt(msg_rcv1,sndpkt1)
    udp.CONN.close()

if __name__ == "__main__":
    rdt_send(input("MESSAGE: "))
