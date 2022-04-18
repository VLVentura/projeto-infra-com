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
    newpkt = udp.Packet("null", udp.CLIENT_PORT,udp.SERVER_PORT, "00000000")
    checksum = udp.checksum([data])

    udt_send(make_pkt(newpkt, data,checksum))

    # State wait for ACK or NAK
    msg_rcv, server_address = udp.CONN.recvfrom(2048)
    print(f"This was sent by {server_address}: {udp.parse_package(msg_rcv)[0]}")
    while (udp.dataIntegrity(msg_rcv) and isNACK) is True or isACK is False:
        udt_send(make_pkt(newpkt, data, checksum))
    udp.CONN.close()

if __name__ == "__main__":
    rdt_send(input("MESSAGE: "))
