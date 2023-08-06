import socket
import os
from socket import socket as funcSocket

# criando buffer, porta e host
buffer_size  = 1024
HOST = 'localhost'
PORT = 5000
orig = (HOST, PORT)

# criando servidor udp
ServidorUdp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
ServidorUdp.bind(orig)

endereco = './servidorFile'

# criando diretório
if not os.path.exists(endereco):
    os.makedirs(endereco)

extention, cliente = ServidorUdp.recvfrom(buffer_size)
extentionFile= extention.decode()

# enquanto o cliente não pediu fim da conexão
while extentionFile != "END" :

    # recebendo arquivo enviado pelo cliente
    with open(f"{endereco}/arquivoNovo.{extentionFile}", 'wb') as f: 
     while True:
        msg, cliente = ServidorUdp.recvfrom(buffer_size)
        if not msg:
            break
        f.write(msg)
        f.flush() 
    f.close()

    # reenviando o arquivo para o cliente
    with open(f"{endereco}/arquivoNovo.{extentionFile}", 'rb') as file:
        dest = cliente  # Utilize o endereço do cliente para enviar a resposta
    
        ServidorUdp.sendto(extention, dest)

        l = file.read(buffer_size)
        while l:
            ServidorUdp.sendto(l, dest)
            l = file.read(buffer_size)
        ServidorUdp.sendto(b'', dest)
        print("Terminei de enviar para o cliente")

    file.close()

    extention, cliente = ServidorUdp.recvfrom(buffer_size)
    extentionFile= extention.decode()
print("Fim da conexão.")
ServidorUdp.close()
