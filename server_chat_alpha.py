import socket

HOST = 'localhost'
PORT = 12000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print('Aguardando Cliente')
conn, ender = s.accept()

print('Conectado em', ender)
token = 0
contaI = 0
contaM = 0
while True:
    data = conn.recv(1024)
    invalid = 'comando invalido\n'
    if data.decode() == 'fechar':
        print('Fechando conexão')
        conn.close()
        break

    elif data.decode() == 'chefia' and token == 0:
        answer = 'Digite sua mesa:\n'
        conn.sendall(str.encode(answer))
        Nmesa = conn.recv(1024)

        answer = 'Digite seu nome:\n'
        conn.sendall(str.encode(answer))
        Nome_mesa = conn.recv(1024)
        
        token = 1
        answer = 'digite uma das opções a seguir:\n1 - Cardápio\n2 - Pedido\n3 - Conta Individual\n4 - Conta da mesa\n'
        conn.sendall(str.encode(answer))
        
    elif data.decode() == '1' and token == 1:
        cardapio = '\n1 - frango grelhado...R$15,00\n2 - Parmegiana........R$20,00\n3 - Bife à cavalo.....R$25,00\n\ndigite uma das opções a seguir:\n1 - Cardápio\n2 - Pedido\n3 - Conta Individual\n4 - Conta da mesa\n'
        conn.sendall(str.encode(cardapio))
    
    elif data.decode() == '2' and token == 1:
        pedido = 'digite o seu pedido\n'
        conn.sendall(str.encode(pedido))

        pedidoR = conn.recv(1024)
        if pedidoR.decode() == '1':
            contaI = contaI + 15.00
        if pedidoR.decode() == '2':
            contaI = contaI + 20.00
        if pedidoR.decode() == '3':
            contaI = contaI + 25.00
   
        conn.sendall(str.encode(answer))
    
    elif data.decode() == '3' and token == 1:
        pagarI = 'Sua conta foi R$' + str(contaI) + ', digite o valor a ser pago\n'
        conn.sendall(str.encode(pagarI))
        
        recebido = conn.recv(1024)
        contaI = float(recebido.decode()) - contaI

        if contaI > 0.00:
            conta = 0.00
            troco = 'Seu troco é de R$' + str(contaI) + '\n'
            conn.sendall(str.encode(troco))
        
        else:
            contaI = -contaI
            falta = 'Faltam R$' + str(contaI) + ' para pagar a conta' + '\n'
            conn.sendall(str.encode(falta))


    elif data.decode() == '4' and token == 1:
        contaM = contaM + contaI
        pagarM = 'Sua conta foi R$' + str(contaI) + ' e a da mesa foi R$' + str(contaM) + ', digite o valor a ser pago' + '\n'

    else:
        conn.sendall(str.encode(invalid))