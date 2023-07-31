import socket
from socket import socket as funcSocket

## Objetivo: Envio de arquivos de até 1024. Se passar dessa quantidade
## Deve ser dividido em pacotes
buffer_size  = 1024
HOST = 'localhost'
PORT = 5000
dest = (HOST, PORT)
## Deve ser feito o IP e porta para que o cliente receba conteudo

udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('localhost',3000)) #Essa informação é para que seja criada um endereço que identifque a porta qye de onde esta sendo encaminada o arquiv inicial. Comunicacao entre processo
'''AF_INET é referente a ser ipv4, sock DGRAM é referente a ser UDP'''

#print("Para sair use ctnl X")
# ALTERAR EXTENSÃO CASO QUERIA ALTERAR O ARQUIVO
endereco = './arquivos/teste.txt'

with open(endereco, 'rb') as f:
    extensao = endereco.split('.')[-1].encode() # aqui é pra pegar a expencao. faco o split de endereco e guardo o nome pos '.'
    udp.sendto(extensao, dest) # envio a string codificada
    l = f.read(buffer_size) # leio o arquivo que vou enviar os bytes. Aqui leio o primeiro pacotes de 1024
    while l:
        print(l)
        udp.sendto(l, dest) # Como eh UDP temos que enviar para a porta referenciada, n ha processo de autenticacao tipo udp.connect(0
        l = f.read(buffer_size) # ler os prox 1024 bytes do arq

udp.close()

## Ainda preciso verificar se realmente esta sendo enviado os pacotes de 1024 em 1024
## Vai receber os arquivos do servidor/cliente e guardar em uma pasta também ?
