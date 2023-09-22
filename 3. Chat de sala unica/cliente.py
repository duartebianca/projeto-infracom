import socket
import random
import os
from socket import socket as funcSocket
import threading
import time 

# criando buffer, porta e host
BUFFER_SIZE  = 1024
HOST = '127.0.0.1'
PORT = 5000
server = (HOST, PORT)

# tempo do timeout
timeout = 1

# criando socket cliente_udp
cliente_udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)

# login do usuário com username e setando a porta
def login():
    username = None
    while username is None:
        username = input("Digite seu nome de usuário: ")

    if username == 'fulano':
        cliente_udp.bind((HOST, 3000))
    elif username == 'sicrano':
        cliente_udp.bind((HOST, 4000))
    else: 
        print("Esse username não foi encontrado")

    return username

# função que pega o input do user
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

# função de geração de erro
def error_gen():
    numero_aleatorio = random.random()
    probabilidade_de_erro = 0.5
    if numero_aleatorio < probabilidade_de_erro:
        return 1
    else: 
        return 0

def snd_pkt(sender, dest, msg, lock): # remetente (quem envia); destinatario (HOST, PORT) - quem recebe o pacote; mensagem
    global timeout
    with lock:
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
                # print('ack')
                pass
            break

def thread_rcv(dest, lock): # destinatario (HOST, PORT) - quem recebe o pacote;
    global timeout
    last_msg = None
    count = 0
    rcv_msg = None
    while True:
        if count == 3:
            time.sleep(1)
            count = 0
        with lock:
            count += 1
            try:
                rcv_msg, sender = dest.recvfrom(BUFFER_SIZE)                    
            except socket.timeout:
                pass
        if rcv_msg is not None: 
            if rcv_msg == last_msg:
                dest.sendto(('ack').encode(), sender)
                rcv_msg = None
            elif 'ack' not in rcv_msg.decode():
                print(rcv_msg.decode())
                # print('ack enviado, para mensagem:', rcv_msg.decode())
                dest.sendto(('ack').encode(), sender)
                last_msg = rcv_msg
            else: 
                pass

def thread_input(sender, dest, lock):
    while True:
        msg = input()
        snd_pkt(sender, dest, msg, lock)    

def main(): 
    cliente_udp.settimeout(timeout)
    lock = threading.Lock()
    username = login()
    print_commands()
    thread1 = threading.Thread(target=thread_input, args=(cliente_udp, server, lock))
    thread2 = threading.Thread(target=thread_rcv, args=(cliente_udp, lock))
    thread2.start()
    thread1.start()

if __name__ == "__main__":
    main()  