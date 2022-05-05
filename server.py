<<<<<<< HEAD
from socket import socket, AF_INET, SOCK_DGRAM
=======
#!/usr/bin/env python3
>>>>>>> rdt3/server
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

if __name__ == "__main__":
    server = Server("localhost", 12000)
    server.run()
