from ast import Pass
from email import message
import socket
from datetime import datetime
from rdt import Rdt

HOST = 'localhost'
PORT = 12000
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((HOST, PORT))
#s.listen()
conn = Rdt.create_server_connection(HOST, PORT)

class client:
    
    def __init__(self,nome, numMesa):
        self.nome = nome
        self.mesa = numMesa
        self.saldo = 0.0
        self.pedidos = ""

    def creditar(self, valor):
        self.saldo -= valor

    def debitar(self, valor):
        self.saldo += valor
    
    def adpedido(self, pedido):
        self.pedidos += pedido + '\n'
        


clientes = []

print('Aguardando Cliente')
mesage, ender = conn.recv()

print('Conectado em', ender)
token = 0
contaI = 0
contaM = 0
conn.send("ACK", ender)
while True:
    mesage, ender = conn.recv()
    invalid = 'comando invalido\n'
    if mesage == 'fechar':
        print('Fechando conexão')
        conn.reset_state_from(ender)
        break

    elif mesage == 'chefia' and token == 0:
        horaMin = datetime.now().strftime("%H:%M")
        answer = horaMin + ' CINtofome: Digite sua mesa:\n'
        conn.send(answer, ender)
        Nmesa, ender = conn.recv()

        horaMin = datetime.now().strftime("%H:%M")
        answer = horaMin + ' CINtofome: Digite seu nome:\n'
        conn.send(answer, ender)
        Nome_mesa, ender = conn.recv()

        novo_cliente = client(Nome_mesa, Nmesa)
        clientes.append(novo_cliente)

        horaMin = datetime.now().strftime("%H:%M")        
        token = 1
        answer = horaMin + ' CINtofome: digite uma das opções a seguir:\n1 - Cardápio\n2 - Pedido\n3 - Conta Individual\n4 - Conta da mesa\n5 - Nao vou pedir nada, pode atender outro cliente\n'
        conn.send(answer, ender)
        
    elif mesage == '1' and token == 1:
        cardapio = '\n1 - frango grelhado...R$15,00\n2 - Parmegiana........R$20,00\n3 - Bife à cavalo.....R$25,00\n\ndigite uma das opções a seguir:\n1 - Cardápio\n2 - Pedido\n3 - Conta Individual\n4 - Conta da mesa\n5 - Nao vou pedir nada, pode atender outro cliente\n'
        conn.send(cardapio, ender)
    
    elif mesage == '2' and token == 1:
        horaMin = datetime.now().strftime("%H:%M")        
        pedido = horaMin + ' CINtofome: digite o seu pedido\n'
        conn.send(pedido, ender)

        pedidoR, ender = conn.recv()
        if pedidoR == '1':
            #contaI = contaI + 15.00
            for clnt in clientes:
                if clnt.nome == Nome_mesa:
                    clnt.debitar(15)
                    clnt.adpedido("Frango grelhado => R$ 15,00")
                    


        if pedidoR == '2':
            #contaI = contaI + 20.00
            for clnt in clientes:
                if clnt.nome == Nome_mesa:
                    clnt.debitar(20)
                    clnt.adpedido("Parmegiana => R$ 20,00")
        
        
        
        if pedidoR == '3':
            #contaI = contaI + 25.00
            for clnt in clientes:
                if clnt.nome == Nome_mesa:
                    clnt.debitar(25)
                    clnt.adpedido("BIfe a cavalo => R$ 25,00")
   
        conn.send(answer, ender)
    
    elif mesage == '3' and token == 1:
        
        horaMin = datetime.now().strftime("%H:%M")
        contaCliente = 0
        for clnt in clientes:
            if clnt.nome == Nome_mesa:
                contaCliente = clnt.saldo

                
        pagarI = horaMin + ' CINtofome: Sua conta foi R$' + str(contaCliente) + ', digite o valor a ser pago\n'
        conn.send(pagarI, ender)
        
        recebido, ender = conn.recv()
        #contaI = float(recebido.decode()) - contaI
        for clnt in clientes:
            if clnt.nome == Nome_mesa:
                clnt.creditar(float(recebido))
    
                if clnt.saldo < 0.00:
                    trocado = clnt.saldo * -1
                    clnt.saldo = 0.00

                    horaMin = datetime.now().strftime("%H:%M")
                    troco = horaMin + ' CINtofome: Seu troco é de R$' + str(trocado) + '\n'
                    conn.send(troco, ender)
        
                else:
                    #contaI = -contaI
                    horaMin = datetime.now().strftime("%H:%M")
                    falta = horaMin + ' CINtofome: Faltam R$' + str(clnt.saldo) + ' para pagar a conta' + '\n'
                    conn.send(falta, ender)


    elif mesage == '4' and token == 1:
        #contaM = contaM + contaI
        horaMin = datetime.now().strftime("%H:%M")
        #pagarM = horaMin + ' CINtofome: Sua conta foi R$' + str(contaI) + ' e a da mesa foi R$' + str(contaM) + ', digite o valor a ser pago' + '\n'
        conta_mesa = horaMin + " CINfome: \n"
        saldo_mesa = 0.0
        for clnt in clientes:
            if clnt.mesa == Nmesa:
                saldo_mesa += clnt.saldo
                conta_mesa += '\n' + str(clnt.nome) + '\n' + clnt.pedidos + '\n' + 'Total: ' + str(clnt.saldo) + '\n'
        
        conta_mesa += '\n' + 'Total Mesa:' + str(saldo_mesa) + '\n'
        
        conn.send(conta_mesa, ender)

    elif mesage == '5' and token == 1:

        horaMin = datetime.now().strftime("%H:%M")
        info = horaMin + ' CINfome: Indo atender outro cliente\n'
        token = 0
        conn.send(info, ender)

    else:
        conn.send(invalid, ender)
