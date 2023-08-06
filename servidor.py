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

# extentionDecoded = extention.decode() # converte extensão p/ string

while extentionFile != "END" :

    # print(str(extention))

    with open(f"{endereco}/arquivoNovo.{extentionFile}", 'wb') as f: 
     while True:
        msg, cliente = ServidorUdp.recvfrom(buffer_size)
        if not msg:
            break
        #print("arquivo teste:", msg.decode('utf-8'))  
        f.write(msg)
        f.flush()   # passei 3 horas tmb por conta dessa desgraça
    f.close()


    with open(f"{endereco}/arquivoNovo.{extentionFile}", 'rb') as file:
        dest = cliente  # Utilize o endereço do cliente para enviar a resposta
    #extention = endereco.split('.')[-1].encode()
    
        ServidorUdp.sendto(extention, dest)

        l = file.read(buffer_size)
        while l:
            ServidorUdp.sendto(l, dest)
            l = file.read(buffer_size)
        ServidorUdp.sendto(b'', dest)
        print("terminei de enviar para o cliente")

    file.close()

    extention, cliente = ServidorUdp.recvfrom(buffer_size)
    extentionFile= extention.decode()
    # extentionDecoded = extention.decode()
print("sai")
ServidorUdp.close()