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

''' 
- Exibir lista de usuários do chat
- Sair da sala
'''

# criando servidor udp
servidor_udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_udp.bind((HOST, PORT))

# timeout
timeout = 0.5
clients_logado = []

def print_chat():
    os.system('cls')
    print("-+>"*12, '\n')
    print("Chat RDT 3.0\n")
    print("<-+"*12, '\n')

def getTime():
    return str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M'))

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

def serv_exist(sender):

    for cliente in clients_logado:
         sender_user = cliente["sender"]
         if sender_user == sender:
            return True
         
    return False

def user_exist(usuario):
    
    for cliente in clients_logado:
        if cliente["usuario"] == usuario:
            return True
        
    return False

def verifica_user(sender, usuario):

    usuario_exist = user_exist(usuario)
    serder_exist = serv_exist(sender)

  
    if usuario_exist and not serder_exist:
         return "invalido"
    elif not usuario_exist and serder_exist:
         return  "existe"
    elif not usuario_exist and not serder_exist:
        return "add"
    else:

        for cliente in clients_logado:
            sender_dado = cliente["sender"]
            user_dado = cliente["usuario"]
            if sender_dado == sender and user_dado == usuario:
               return  "existe" 
            
        return "invalido"
           
def verifica_tipo(sender, msg):
    
    msg_rcv = msg.split()[0] ## verificar isso. e se vir uma frase sem espaco?
  
    if 'login_as' == msg_rcv:
        usuario = msg.split()[1] #pegando o usuario

        exist = verifica_user(sender, usuario)

        if exist == "invalido":
            msg_final = f"Nome de Login <{usuario}> já existe#exced1124"
            print(msg_final)
        elif exist == "existe":
            msg_final = f"Voce já esta logado#exced1124"
        else:
            print("a pessoa nao existe")
            cliente = {"sender": sender, "usuario": str(usuario)}
            clients_logado.append(cliente)
            msg_final = f"{usuario} entrou na sala#exced112"
    else:
       # se for mensagem normal não teremos usuario. usuario será nulo
       for cliente in clients_logado:
         if cliente["sender"] == sender:
            usuario = cliente["usuario"]
            print(cliente)
            break
       #user_snd = [user for user in clients_logado if user["sender"] == sender]
       #print(user_snd)
      
       msg_final = f"<{sender}>/~{usuario}:<{msg}><{getTime()}>#exced112"
    
    return sender, msg_final, usuario
        
def rcv_pkt_server(dest): # destinatario (HOST, PORT) - quem recebe o pacote
    dest.settimeout(None)
    while True:
        rcv_msg, sender = dest.recvfrom(BUFFER_SIZE)
        
        rcv_msg = rcv_msg.decode()

       #  print("rcv_pkt_server:", rcv_msg, sender)
        
        if 'ack' not in rcv_msg:  
            print("enviando ack de recebimento..") 
            dest.sendto(('ack#').encode(), sender)
            result = verifica_tipo(sender, rcv_msg) #retorna o retorno de verofica tipo
            return result
        
     
## A minha ideia eh o cliente receber a mensagem do servidor, (usuario), serder
## assim conseguimos separar o nome do usuario para cliente consultar
## estou colocando uns sufixos como se fosse um protocolo de identificação de mensagem

def main():

    print_chat()
    while True:
        sender, dec_msg, user = rcv_pkt_server(servidor_udp)

        msg = dec_msg.rsplit('#', 1)[0]
        msg_final = f"{msg}#{user}"
    
        
       
        print("Na main do server", dec_msg.rsplit('#', 1)[1])

        if(dec_msg.rsplit('#', 1)[1] == "exced1124"):
            snd_pkt(servidor_udp, sender, msg_final)
        else:
            chat_clients = clients_logado
            for client in chat_clients:
               # snd_pkt(servidor_udp, client, 'mensagem aleatoria ' + str(int(random.random()*100)))
             # coloquei . para modularizar para que o usuario tenha acesso ao nome de quem enviou msg
                print("aqui")
                print(client)
                snd_pkt(servidor_udp, client["sender"], msg_final)
            

if __name__ == "__main__":
    main()  