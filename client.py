import socket
from rdt import Rdt

HOST = "localhost"
PORT = 12000
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST, PORT))
conn = Rdt.create_client_connection(HOST, PORT)


message = input('Digite o comando\n')
#s.sendall(str.encode(message))
conn.send(message)
while True:
    if message == 'fechar':
        break
    #answer = s.recv(1024)
    #answer = conn.recv()
    answer, ender = conn.recv()
    print(answer)
    message = input()
    conn.send(message, ender)


