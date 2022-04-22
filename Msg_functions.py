import socket
import struct

PAYLOAD = 1000  # size of data payload of the RDT layer
TYPE_DATA = 12  # 12 means data
MSG_FORMAT = 'B?HH'  # Format string for header structure

def __udt_recv(sockd, length):  #socket com a msg e tamanho max da msg
    (rmsg, peer) = sockd.recvfrom(length)
    return rmsg                 #Retorna byte de msg recebido

def __cut_msg(byte_msg):        #Input: mensagem no formato de byte
    global PAYLOAD
    if len(byte_msg) > PAYLOAD:
        msg = byte_msg[0:PAYLOAD]
    else:
        msg = byte_msg
    return msg                  #Retorna a msg no tamanho <= ao imposto

def __make_data(seq_num, data):
    global TYPE_DATA, MSG_FORMAT

    msg_format = struct.Struct(MSG_FORMAT) #Msg inicial
    checksum = 0  #First set checksum to 0
    init_msg = msg_format.pack(TYPE_DATA, seq_num, checksum, socket.htons(len(data))) + data #.pack converte o valor 2 em diante no formato do 1o valor
    #header = type(1) + seq(1) + checksum(2) + payloadlen(2) = 6 bytes

    #Calculo checksum
    checksum = __int_chksum(bytearray(init_msg)) #passa a mensagem inicial para o checksum fazer a "aglutinação"

    #Msg com checksum final
    complete_msg = msg_format.pack(TYPE_DATA, seq_num, checksum, socket.htons(len(data))) + data #hton = host to network byte order
    return complete_msg #Msg com o header + data

def __unpack_helper(msg):   #"destrincha" a msg recebida
    global MSG_FORMAT
    size = struct.calcsize(MSG_FORMAT)
    (msg_type, seq_num, recv_checksum, payload_len), payload = struct.unpack(MSG_FORMAT, msg[:size]), msg[size:] #unpack descompacta de acordo com o formato, precisa ter tamanho equivalente ao do calczise
    return (msg_type, seq_num, recv_checksum, socket.ntohs(payload_len)), payload  # ntohs = network to host byte order

def __has_seq(recv_msg, seq_num):   #Checa se o pacote recebido contem o sequence equivalente ao sequence real
    (msg_type, recv_seq_num, _, _), _ = __unpack_helper(recv_msg)
    return recv_seq_num == seq_num

def __is_data(recv_pkt, seq_num):   #Checa se a msg é dado ou não
    global TYPE_DATA
    (pkt_type, pkt_seq, _, _), _ = __unpack_helper(recv_pkt)
    return pkt_type == TYPE_DATA and pkt_seq == seq_num #true or false

