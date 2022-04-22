from socket import socket, AF_INET, SOCK_DGRAM
from rdt import Rdt


class Client:
    def __init__(self, server_address: str, server_port: int, timeout: int = 10):
        self.__server_info = (server_address, server_port)
        self.__timeout = timeout
        self.__conn = None
        self.__rdt = None

    def run(self):
        self.__start_connection()
        self.__start_client()

    def __start_connection(self) -> socket:
        self.__conn = socket(AF_INET, SOCK_DGRAM)
        self.__conn.settimeout(self.__timeout)
        self.__conn.bind(("", 0))
        self.__rdt = Rdt(self.__conn)

    def __start_client(self):
        while True:
            self.__rdt.send(self.__server_info, "Hello World - 1")
            # sleep(1)
            # self.__rdt.send(self.__server_info, "Hello World - 2")


if __name__ == "__main__":
    client = Client("localhost", 12000, 2)
    client.run()
