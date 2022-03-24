from socket import socket, AF_INET, SOCK_DGRAM
from checksum import checksum

server_name = "localhost"
server_port = 12000
message = "Hello from client!"

conn = socket(AF_INET, SOCK_DGRAM)
conn.sendto(message.encode(), (server_name, server_port))

msg_received, server_address = conn.recvfrom(2048)
print(f"Message recieved from {server_address}: {msg_received.decode()}")

conn.close()
