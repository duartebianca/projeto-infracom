import socket
from socket import socket as funcSocket

## Envio de arquivos de até 1024. Se passar dessa quantidade é dividido em pacotes
buffer_size  = 1024
HOST = 'localhost'
PORT = 5000
dest = (HOST, PORT)

# Criando socket do UDP
udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('localhost',3000)) #Essa informação é para que seja criada um endereço que identifque a porta qye de onde esta sendo encaminada o arquiv inicial. Comunicacao entre processo
'''AF_INET é referente a ser ipv4, sock DGRAM é referente a ser UDP'''

# ALTERAR EXTENSÃO CASO QUERIA ALTERAR O ARQUIVO
endereco = './arquivos/teste.txt'

with open(endereco, 'rb') as f:
    extensao = endereco.split('.')[-1].encode() # pegando extensão
    udp.sendto(extensao, dest) # envio da string codificada
    l = f.read(buffer_size) # lendo o primeiro pacotes de 1024 bytes
    while l:
        print(l)
        udp.sendto(l, dest) # enviando para a porta referenciada
        l = f.read(buffer_size) # ler os prox 1024 bytes do arq
    udp.sendto(b'', dest) # arquivo vazio para indicar fim
f.close()


endereco = './ClienteFile'

if not os.path.exists(endereco):
    os.makedirs(endereco)

extention, servidor = udp.recvfrom(buffer_size)
# print(servidor)

# colocar logica para que multiplos arquivos sejam enviados e guardados
# colocar um while no servidor para ficar enviando e recebendo arquivos até determinada entrada
# sempre incrementar o i para distinguir os arquivos

with open(f"{endereco}/arquivoNovo.{extention.decode()}", 'wb') as f:
    while True:
        msg, servidor = udp.recvfrom(buffer_size)
        if not msg:
            break
       #  print(msg)
        f.write(msg)
        f.flush()

udp.close()