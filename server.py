from socket import socket, AF_INET, SOCK_DGRAM
from rdt import Rdt


class Server:
    def __init__(self, address: str, port: int):
        self.__address = address
        self.__port = port
        self.__conn = None
        self.__rdt = None

    def run(self):
        self.__start_connection()
        self.__start_server()

    def __start_connection(self) -> socket:
        self.__conn = socket(AF_INET, SOCK_DGRAM)
        self.__conn.bind((self.__address, self.__port))
        self.__rdt = Rdt(self.__conn)

    def __start_server(self):
        print(f"Server is listening on port: {self.__port}")

        while True:
            data, client_address = self.__rdt.recv()
            print(data)
            # self.__rdt.send(client_address, data)


def parse_package(message: bytes) -> tuple:
    return message.decode().split("\x01")


if __name__ == "__main__":
    server = Server("localhost", 12000)
    server.run()
