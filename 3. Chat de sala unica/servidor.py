import socket
import random
import os
from socket import socket as funcSocket
import datetime
from collections import defaultdict

# criando buffer, porta e host
BUFFER_SIZE  = 1024
HOST = '127.0.0.1'
PORT = 5000

# criando servidor udp
servidor_udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_udp.bind((HOST, PORT))

# timeout
timeout = 0.5
clients_logado = []


# definindo os parâmetros para o ban
countBans = {} #contador de votos
banTable = [] #lista de banidos
voteTable = defaultdict(list)

# lista de amigos por usuário
amigos_por_usuario = {}

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

# funcao que verifica se a porta do cliente existe
def port_exist(sender):
    for cliente in clients_logado:
         sender_user = cliente["sender"]
         if sender_user == sender:
            return True
         
    return False

# funcao que verifica se o username do cliente existe
def username_exist(usuario):
    for cliente in clients_logado:
        if cliente["usuario"] == usuario:
            return True
        
    return False

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
            # caso contrario tenta reenviar
            if error_gen() == 0:
                sender.sendto(msg.encode(), dest)

# funcao que verifica o usuario informado
def verifica_user(sender, usuario):
    usuario_exist = username_exist(usuario)
    serder_exist = port_exist(sender)
  
    if usuario_exist and not serder_exist: # usuario nao eh valido
        return "invalido"
    elif not usuario_exist and serder_exist: # tentativa de logar com nome diferente
        return  "existe"
    elif not usuario_exist and not serder_exist:
        return "add"
    else:
        # tentativa de logar estando logado
        for cliente in clients_logado:
            sender_dado = cliente["sender"]
            user_dado = cliente["usuario"]
            if sender_dado == sender and user_dado == usuario:
               return  "existe" 
            
        return "invalido"

# funcao do estado da lista de amigos
def process_mylist_request(sender):
    if sender in amigos_por_usuario:
        friends_list = amigos_por_usuario[sender]
        if friends_list == []:
          response_msg = "Sua lista de amigos está vazia."
        else:
          response_msg = "Sua lista de amigos:\n" + "\n".join(friends_list)
    else:
        response_msg = "Sua lista de amigos está vazia."
    return response_msg

# adicao e remocao na lista de amigos
def manipulate_list(sender, msg):
    msg_rcv = msg.split()[0]
    if msg_rcv == 'addtomylist':
        usuario = msg.split()[1]
        if username_exist(usuario):
          if sender in amigos_por_usuario:
              amigos_por_usuario[sender].append(usuario)
              msg_final = f"{usuario} tornou-se amigo."
          else:
              amigos_por_usuario[sender] = [usuario]
              msg_final = f"{usuario} tornou-se amigo."
        else:
          msg_final = f"O usuário '{usuario}' não está logado."
    elif msg_rcv == 'rmvfrommylist':
        usuario = msg.split()[1] 
        if sender in amigos_por_usuario:
            if usuario in amigos_por_usuario[sender]:
                amigos_por_usuario[sender].remove(usuario)
                msg_final = f"{usuario} foi removido."
            else:
                msg_final = f"{usuario} não está na lista."
    return sender, msg_final, usuario          

# funcao de logar no chat
def login_as(sender, usuario):
    exist = verifica_user(sender, usuario)

    # so consegue logar se nao tiver sido banido
    if usuario not in banTable:
        if exist == "invalido": # logando com usuario que esta sendo  utilizado
            msg_final = f"Nome de Login <{usuario}> já existe#exced1124"
        elif exist == "existe": # logando quando ja esta logado
            msg_final = f"Voce já esta logado#exced1124"
        else:
            # logando
            cliente = {"sender": sender, "usuario": str(usuario)}
            clients_logado.append(cliente)
            msg_final = f"{usuario} entrou na sala#exced112"
    else:
        return sender, "", False

    return sender, msg_final, usuario

# funcao de banir usuario
def ban_user(usuario, sender):
    exist = username_exist(usuario)


    if exist == True:
        # Meta da contagem de ban
        meta = int(0.5 * len(clients_logado)) + len(clients_logado)%2 
        
        if usuario not in banTable and sender not in voteTable[usuario]:
            for client in clients_logado:
                client_user = client["usuario"]
                if client_user == usuario:
                    # primeiro voto para ser banido
                    if client_user not in countBans:
                        countBans[client_user] = 1
                        msg_final = f"[{client_user}] ban {str(countBans[client_user])}/{str(meta)}#exced112"
                    # nao eh o primeiro voto, apenas adicionando na contagem de votos
                    else:
                        (countBans[client_user]) = countBans[client_user] + 1
                        msg_final = f"[{client_user}] ban {str(countBans[client_user])}/{str(meta)}#exced112"

                    voteTable[usuario].append(sender)

                    if countBans[client_user] >= meta:
                        banTable.append(client_user)
                        # enviando mensagem para usuario banido
                        msg_banido = "Você foi banido!"
                        snd_pkt(servidor_udp, client["sender"], msg_banido)
                        # enviando mensagem para os outros que estão logados
                        clients_logado.remove(client)
                        msg_final = (f"{client_user} foi banido da sala!#exced112")
            return msg_final
        else:
            msg = "Nao pode votar mais de uma vez"
            return msg 
    else:
        msg = "Nao eh possivel expulsar quem nao esta no chat.#exced112"
        return msg 

# funcao de sair do chat
def disconnect(sender):
    for client in clients_logado:
        client_sender = client["sender"]
        client_user = client["usuario"]
        if client_sender == sender:
            clients_logado.remove(client)
            # mensagem para quem saiu
            msg_client = "Você saiu do chat!"
            snd_pkt(servidor_udp, client_sender, msg_client)
            # mensagem para os outros
            msg_final = f"{client_user} saiu do chat!#exced112"
    return client_sender, msg_final, client_user

# funcao de apresentar a lista de usuarios logados
def chat_list(sender):
    msg_final = "\nLista de usuarios:\n"

    for client in clients_logado:
        usuario_logado = client["usuario"]
        msg_final += f"- {usuario_logado}\n"

        if client["sender"] == sender:
            client_user = client["usuario"]
    
    snd_pkt(servidor_udp, sender, msg_final)
    return client_user

# verifica mensagem enviada pelo cliente e como sera tratada
def verify_command(sender, msg):
  
    # hi, meu nome eh <nome_usuario>
    if msg.startswith('hi, meu nome eh '):
        usuario = msg.split()[-1] # pegando o usuario
        info = login_as(sender, usuario)
        return info
    # ban <nome_usuario>
    elif msg.startswith("ban"): 
        usuario = msg.split()[-1] # pegando o usuario
        info = ban_user(usuario, sender)

        # envia a mensagem apenas para o usuario que solicitou o comando
        if info.startswith("Nao eh possivel expulsar") or info.startswith("Nao pode votar "):
            return sender, info, None

        return sender, info, usuario
    # bye    
    elif msg.startswith("bye"):
        info = disconnect(sender)
        return info
    else:
       for cliente in clients_logado:
         if cliente["sender"] == sender:
            usuario = cliente["usuario"]
            break
      
       msg_final = f"<{sender}>/~{usuario}:<{msg}><{getTime()}>#exced112"
       return sender, msg_final, usuario

# recebimento de pacotes       
def rcv_pkt_server(dest): 
    dest.settimeout(None)
    while True:
        rcv_msg, sender = dest.recvfrom(BUFFER_SIZE)
        
        rcv_msg = rcv_msg.decode()
        
        if rcv_msg == "mylist":
          response_msg = process_mylist_request(sender)
          snd_pkt(dest, sender, response_msg)
        elif rcv_msg.startswith("addtomylist ") or rcv_msg.startswith("rmvfrommylist "):
          sender, response_msg, usuario = manipulate_list(sender, rcv_msg)
          snd_pkt(dest, sender, response_msg) 
        elif rcv_msg == "list":
            chat_list(sender)      
        elif 'ack' not in rcv_msg: 
            if port_exist(sender): 
                dest.sendto(('ack').encode(), sender)
                result = verify_command(sender, rcv_msg)
                return result
            else:
                if not rcv_msg.startswith('hi, meu nome eh '):
                    return sender, rcv_msg, False
                else:
                    result = verify_command(sender, rcv_msg)
                    return result

def main():

    print_chat()
    while True:

        sender, dec_msg, user = rcv_pkt_server(servidor_udp)

        if user == None:
            snd_pkt(servidor_udp, sender, dec_msg)
        elif user:
            msg = dec_msg.rsplit('#', 1)[0]
      

            if(len(dec_msg.rsplit('#', 1)) == 2 and dec_msg.rsplit('#', 1)[1] == "exced1124"):
                 snd_pkt(servidor_udp, sender, msg)
            else:
                chat_clients = clients_logado
                for client in chat_clients:
         
                    if dec_msg.startswith(f"<{sender}>") and dec_msg.rsplit("#", 1)[1]== "exced112":

                        first = dec_msg.split("/")[0]
                        second = dec_msg.split("/")[1]

                        if client["sender"] in amigos_por_usuario:
                            if sender != client["sender"] and user in amigos_por_usuario[client["sender"]]: 
                                msg_final = first + "/" + "[Amigo]" + second
                                snd_pkt(servidor_udp, client["sender"], msg_final)
                            else:
                               if sender!=client["sender"]:
                                snd_pkt(servidor_udp, client["sender"], msg)
                               else:
                                   pass
                        else:
                               if sender!=client["sender"]:
                                snd_pkt(servidor_udp, client["sender"], msg)
                               else:
                                   pass
                    else:
                        snd_pkt(servidor_udp, client["sender"], msg)
        else:
            msg = "Não foi possível acessar o chat."
            snd_pkt(servidor_udp, sender, msg)

if __name__ == "__main__":
    main()  