import socket

HOST = "localhost"
PORT = 12000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

message = input('Digite o comando\n')
s.sendall(str.encode(message))
while True:
    if message == 'fechar':
        break
    answer = s.recv(1024)
    message = input(answer.decode())
    s.sendall(str.encode(message))


