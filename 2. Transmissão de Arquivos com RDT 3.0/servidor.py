import socket
import os
from socket import socket as funcSocket

# criando buffer, porta e host
BUFFER_SIZE  = 1024
HOST = 'localhost'
PORT = 5000
orig = (HOST, PORT)

# rdt
next_seq = 0 # enviado
snd_base = 0 # recebido
rcv_base = 0 # recebido

# criando servidor udp
servidor_udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_udp.bind(orig)

endereco = './servidorFile'

# criando diretório
if not os.path.exists(endereco):
    os.makedirs(endereco)

def incrementa(val):
    return 1 - val

def rcv_pkt():
    global rcv_base, snd_base, next_seq
    msg, cliente = servidor_udp.recvfrom(BUFFER_SIZE)
    msg = msg.decode()
    if int(msg[:2]) == rcv_base:
        rcv_base = incrementa(rcv_base)
        # if snd_base == int(msg[2:4]):
            # print('ack recebido!')
    servidor_udp.sendto((str(next_seq).zfill(2) + str(rcv_base).zfill(2)).encode(), cliente)
    
    print(next_seq, rcv_base, '<- next_seq, rcv_base (server)')
    next_seq = incrementa(next_seq)
    return str(msg[4:]) 

def main():
    print("Servidor esperando conexão")
    global rcv_base, next_seq
    # print('main')
    # criando diretório
    if not os.path.exists(endereco):
        os.makedirs(endereco)

    # sync
    syn, cliente = servidor_udp.recvfrom(BUFFER_SIZE)
    # print(syn[:3])
    if syn[:3] == 'syn':
        rcv_base = incrementa(rcv_base)
    synack_next_seq_rcv_base = ('synack' + str(next_seq).zfill(2) + str(rcv_base).zfill(2)).encode()
    servidor_udp.sendto(synack_next_seq_rcv_base, cliente)
    next_seq = incrementa(next_seq)

    extentionFile = rcv_pkt()
    print('extentionFile:', extentionFile)
    # enquanto o cliente não pediu fim da conexão
    while extentionFile != "END" :
        # recebendo arquivo enviado pelo cliente
        with open(f"{endereco}/arquivoNovo.{extentionFile}", 'wb') as f:

            while True:
                msg = rcv_pkt()
                # print(len(msg))
                # msg = msg.encode()
                if not msg:
                    break
                f.write(msg.encode())
                f.flush() 
            f.close()
        print('arquivo recebido!')
        # reenviando o arquivo para o cliente
        with open(f"{endereco}/arquivoNovo.{extentionFile}", 'rb') as file:
            dest = cliente  # Utilize o endereço do cliente para enviar a resposta
        
            servidor_udp.sendto(extentionFile.encode(), dest) 

            l = file.read(BUFFER_SIZE)
            while l:
                servidor_udp.sendto(l, dest)
                l = file.read(BUFFER_SIZE)
            servidor_udp.sendto(b'', dest)
            print("Terminei de enviar para o cliente")

        file.close()

        extentionFile = rcv_pkt()

    print("Fim da conexão.")
    servidor_udp.close()

if __name__ == "__main__":
    main()  