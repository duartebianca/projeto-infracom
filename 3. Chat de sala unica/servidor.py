import socket
import random
import os
from socket import socket as funcSocket
import datetime
import time

# criando buffer, porta e host
BUFFER_SIZE  = 1024
HOST = 'localhost'
PORT = 5000
orig = (HOST, 3000)

# criando servidor udp
servidor_udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_udp.bind((HOST, PORT))

# timeout
timeout = 3

def print_chat():
    os.system('cls')
    print("-+>"*12, '\n')
    print("Chat RDT 3.0\n")
    print("<-+"*12, '\n')

def getTime():
    return str(datetime.datetime.now().strftime('%X'))

def error_gen():
    numero_aleatorio = random.random()
    probabilidade_de_erro = 0.5
    if numero_aleatorio < probabilidade_de_erro:
        return 1
    else: 
        return 0

def snd_pkt(sender, dest, msg): # remetente (quem envia); destinatario (HOST, PORT) - quem recebe o pacote; mensagem
    global timeout
    sender.settimeout(timeout)
    if error_gen() == 0:
        # print('mensagem enviada:', msg)
        sender.sendto((msg).encode(), dest)
    while True:
        try:
            mensagemRecebida, _ = sender.recvfrom(BUFFER_SIZE)
            decode = mensagemRecebida.decode()
            # print(decode, 'msg', ('ack' in decode))
            if 'ack' in decode:
                sender.settimeout(None)
                # print('ack recebido para', decode, 'return')
                return
        except socket.timeout:
            # print('except')
            if error_gen() == 0:
                # print('mensagem enviada:', msg)
                sender.sendto((msg).encode(), dest)     

def rcv_pkt_server(dest): # destinatario (HOST, PORT) - quem recebe o pacote
    dest.settimeout(None)
    # print('None')
    while True:
        rcv_msg, sender = dest.recvfrom(BUFFER_SIZE)
        dec_msg = rcv_msg.decode()
        if 'ack' not in dec_msg:
            dest.sendto(('ack').encode(), sender)
            return sender, dec_msg
        

def main():
    print_chat()
    while True:
        sender, dec_msg = rcv_pkt_server(servidor_udp)
        print(sender, dec_msg, getTime())
        # função de mandar para todos os conectados
        snd_pkt(servidor_udp, orig, 'mensagem aleatoria ' + str(int(random.random()*100)))

if __name__ == "__main__":
    main()  