#!/usr/bin/env python3
from rdt import Rdt


class Server:
    def __init__(self, address: str, port: int):
        self.__port = port
        self.__conn = Rdt.create_server_connection(address, port)

    def run(self):
        print(f"Server is listening on port: {self.__port}")

        while True:
            data, client_address = self.__conn.recv()
            print(f"Msg received from: {client_address}: {data}")


# def server_wait_for_0_from_below(server):
#     rcvpkt, address = Transfer.rcv(server)
#     newIntegrityCheck = Integrity()
#     newManipulation = Manipulation(rcvpkt)
#     while True:
#         if(Integrity.corrupt(newIntegrityCheck,rcvpkt) and
#         Integrity.has_seq1(newIntegrityCheck,rcvpkt)):
#             Transfer.set_segnum(server, 1)
#             Transfer.send(server,"ACK")
#             Transfer.set_add(server, address)
#             rcvpkt, address = Transfer.rcv(server)

#         elif(Integrity.notcorrupt(newIntegrityCheck,rcvpkt) and
#             Integrity.has_seq0(newIntegrityCheck,rcvpkt)):
#             newManipulation.extract()
#             newManipulation.deliver_data()
#             Transfer.set_segnum(server, 0)
#             Transfer.send(server, "ACK")
#             server_wait_for_1_from_below(server)

# def server_wait_for_1_from_below(server):
#     rcvpkt, address = Transfer.rcv(server)
#     newIntegrityCheck = Integrity()
#     newManipulation = Manipulation(rcvpkt)
#     while True:
#         if(Integrity.corrupt(newIntegrityCheck,rcvpkt) and
#         Integrity.has_seq0(newIntegrityCheck,rcvpkt)):
#             Transfer.set_segnum(server, 0)
#             Transfer.send(server,"ACK")
#             Transfer.set_add(server, address)
#             rcvpkt, address = Transfer.rcv(server)

#         elif(Integrity.notcorrupt(newIntegrityCheck,rcvpkt) and
#             Integrity.has_seq1(newIntegrityCheck,rcvpkt)):
#             newManipulation.extract()
#             newManipulation.deliver_data()
#             Transfer.set_segnum(server, 1)
#             Transfer.send(server, "ACK")
#             server_wait_for_0_from_below(server)

# def server_start():
#     server = Transfer(server_port=SERVER_PORT,server_name=SERVER_NAME)
#     server.bind_socket()
#     while True:
#         print(f'LISTENING TO REQUESTS in: {SERVER_PORT}')
#         server_wait_for_0_from_below(server)

if __name__ == "__main__":
    server = Server("localhost", 12000)
    server.run()
