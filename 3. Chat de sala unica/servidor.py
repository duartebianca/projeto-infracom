import socket
import random
import os
from socket import socket as funcSocket
import datetime
import time

# criando buffer, porta e host
BUFFER_SIZE  = 1024
HOST = '127.0.0.1'
PORT = 5000

# criando servidor udp
servidor_udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_udp.bind((HOST, PORT))

# timeout
timeout = 0.5
clients = [(HOST, 3000), (HOST, 4000)]
clients_logado = []

def print_chat():
    os.system('cls')
    print("-+>"*12, '\n')
    print("Chat RDT 3.0\n")
    print("<-+"*12, '\n')

def getTime():
    return str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M'))

# funcao de geracao de erro
def error_gen():
    numero_aleatorio = random.random()
    probabilidade_de_erro = 0.5
    if numero_aleatorio < probabilidade_de_erro:
        return 1
    else: 
        return 0

# funcao de envio de pacotes
def snd_pkt(sender, dest, msg): 
    global timeout
    sender.settimeout(timeout)

    if error_gen() == 0:
        sender.sendto(msg.encode(), dest) 

    while True:
        try:
            mensagemRecebida, remetente = sender.recvfrom(BUFFER_SIZE)
            decode = mensagemRecebida.decode()
            # verifica se o ack foi do usuario que encaminhou
            if 'ack' in decode and remetente == dest: 
                sender.settimeout(None)
                return
        except socket.timeout:
            #caso contrario tenta reenviar
            if error_gen() == 0:
                sender.sendto(msg.encode(), dest)

# funcao que verifica qual tipo de mensagem recebida (commando ou nao)
def verifica_tipo(sender, msg):
    msg_rcv = msg.split()[0]
  
    if 'login_as' in msg_rcv:
        usuario = msg.split()[1] # pegando o usuario
        cliente = {"sender": sender, "usuario": str(usuario)}
        clients_logado.append(cliente)
        msg_final = f"{usuario} entrou na sala"

    # ADICIONAR OS OUTROS COMANDOS POSSIVEIS COM ELIF AQUIX
    
    else:
       # se for mensagem normal não teremos usuario. usuario será nulo
       for cliente in clients_logado:
         if cliente["sender"] == sender:
            usuario = cliente["usuario"]
            print(cliente)
            break
      
       msg_final = f"<{sender}>/~{usuario}:<{msg}><{getTime()}>"
    
    return sender, msg_final, usuario
        
# funcao de recebimento do pacote
def rcv_pkt_server(dest): 
    dest.settimeout(None)
    while True:
        rcv_msg, sender = dest.recvfrom(BUFFER_SIZE)
        
        rcv_msg = rcv_msg.decode()

        print("rcv_pkt_server:", rcv_msg, sender)
        
        if 'ack' not in rcv_msg:  
            dest.sendto(('ack#').encode(), sender)
            result = verifica_tipo(sender, rcv_msg)
            return result
        
     
## A minha ideia eh o cliente receber a mensagem do servidor, (usuario), serder
## assim conseguimos separar o nome do usuario para cliente consultar
def main():
    print_chat()
    while True:
        sender, dec_msg, user = rcv_pkt_server(servidor_udp)
        
        for client in clients_logado:
            msg = f"{dec_msg}#{user}" # coloquei . para modularizar para que o usuario tenha acesso ao nome de quem enviou msg
            snd_pkt(servidor_udp, client["sender"], msg)
            print(sender, client)

if __name__ == "__main__":
    main()  