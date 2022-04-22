from socket import socket, AF_INET, SOCK_DGRAM
from checksum import checksum

ERROR_MESSAGE = "Checksum is not equal."
SUCCESS_MESSAGE = "Checksum is equal."


def parse_package(message: bytes) -> tuple:
    return message.decode().split("\x01")


if __name__ == "__main__":
    server_port = 12000
    conn = socket(AF_INET, SOCK_DGRAM)
    conn.bind(("", server_port))

    print(f"Server is listening on port: {server_port}")
    while True:
        package, client_address = conn.recvfrom(2048)
        client_message, message_checksum = parse_package(package)
        print(f"Message recieved from {client_address}")

        msg_to_send = ""
        if message_checksum == checksum([client_message]):
            msg_to_send = SUCCESS_MESSAGE
        else:
            msg_to_send = ERROR_MESSAGE

        conn.sendto(msg_to_send.encode(), client_address)
