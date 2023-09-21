import socket
import random
import os
from socket import socket as funcSocket

# criando buffer, porta e host
BUFFER_SIZE  = 1024
HOST = 'localhost'
PORT = 5000
server = (HOST, PORT)

# criando socket cliente_udp
cliente_udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
cliente_udp.bind((HOST, 3000))

# tempo do timeout
timeout = 2

# função que pega o input do user e define o arquivo desejado
def print_commands():
    os.system('cls')
    print("-+>"*12, '\n')
    print("Comandos disponiveis:\n")
    print("login_as <nome_do_usuario>")
    print("add_friend <nome_do_usuario>")
    print("rmv_friend <nome_do_usuario>")
    print("ban_user <nome_do_usuario>")
    print("disconnect")
    print("chat_list")
    print("friends_list")
    print("help\n")
    print("<-+"*12, '\n')

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
    print_commands()
    while True:
        command = input()
        snd_pkt(cliente_udp, server, command)     

if __name__ == "__main__":
    main()  