import socket
import random
import os
from socket import socket as funcSocket

# criando buffer, porta e host
BUFFER_SIZE  = 1024
HOST = 'localhost'
PORT = 5000
orig = (HOST, PORT)

# criando servidor udp
servidor_udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_udp.bind(orig)

def print_chat():
    os.system('cls')
    print("-+>"*12, '\n')
    print("Chat RDT 3.0\n")

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
        sender.sendto((msg).encode(), dest)
    flag = 0
    while True:
        while flag == 0:
            try:
                rcv_msg, _ = sender.recvfrom(BUFFER_SIZE)
                flag = 1
            except socket.timeout:
                if error_gen() == 0:
                    sender.sendto((msg).encode(), dest)
        dec_msg = rcv_msg.decode()
        if dec_msg == 'ack':
            sender.settimeout(None)
            break

def rcv_pkt(dest): # destinatario (HOST, PORT) - quem recebe o pacote
    rcv_msg, sender = dest.recvfrom(BUFFER_SIZE)
    dec_msg =  rcv_msg.decode()
    dest.sendto(('ack').encode(), sender)
    return sender, dec_msg


def main():
    print_chat()
    while True:
        sender, dec_msg = rcv_pkt(servidor_udp)
        print(sender, dec_msg)


if __name__ == "__main__":
    main()  