from socket import socket, AF_INET, SOCK_DGRAM
from checksum import checksum


def get_package(message: str) -> bytes:
    msg_to_send = message + "\x01" + checksum([message])
    return msg_to_send.encode()


def send_valid_checksum(conn: socket):
    message = input("Valid checksum - Enter text: ")
    conn.sendto(get_package(message), (server_name, server_port))


def send_not_valid_checksum(conn: socket):
    message = input("Not valid checksum - Enter text: ")
    msg_to_send = message + "\x01" + "100011010100101010"
    conn.sendto(msg_to_send.encode(), (server_name, server_port))


if __name__ == "__main__":
    server_name = "localhost"
    server_port = 12000
    conn = socket(AF_INET, SOCK_DGRAM)

    for i in range(2):
        if i == 0:
            send_valid_checksum(conn)
        else:
            send_not_valid_checksum(conn)

        msg_received, server_address = conn.recvfrom(2048)
        print(f"Message recieved from {server_address}: {msg_received.decode()}")

    conn.close()
