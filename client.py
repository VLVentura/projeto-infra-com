#!/usr/bin/env python3
from time import sleep
from rdt import Rdt


class Client:
    def __init__(self, server_addr: str, server_port: int):
        self.__server_info = (server_addr, server_port)
        self.__conn = Rdt.create_client_connection(server_addr, server_port)

    def run(self):
        while True:
            self.__conn.send("Hello World!")
            sleep(1)


if __name__ == "__main__":
    client = Client("localhost", 12000)
    client.run()
