from socket import socket, AF_INET, SOCK_DGRAM
from checksum import checksum

server_port = 12000

conn = socket(AF_INET, SOCK_DGRAM)
conn.bind(("", server_port))
message = "Hello from Server!"

print(f"Server is listening on port: {server_port}")

while True:
    client_message, client_address = conn.recvfrom(2048)
    print(f"Message recieved from {client_address}: {client_message.decode()}")
    conn.sendto(message.encode(), client_address)
