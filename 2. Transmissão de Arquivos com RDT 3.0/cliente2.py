import socket
import os
from socket import socket as funcSocket

# configurações da conexão
BUFFER_SIZE  = 1024

HOST = 'localhost'
PORT = 5000
server = (HOST, PORT)

# rdt
next_seq = 0 # enviado
snd_base = 0 # recebido
rcv_base = 0 # recebido

# criando socket cliente_udp
cliente_udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
cliente_udp.bind((HOST ,3000))

# função que pega o input do user e define o arquivo desejado
def define_file():

    filesFolder = ""

    print("Escreva o nome do arquivo que quer receber:\n")
    print("Opções disponíveis:")
    print("- testePDF.pdf")
    print("- testeTXT.txt")
    print("- testeMP3.mp3")
    print("- testeIMG.jpeg\n")
    print("Ou finalize a conexão com")
    print("- Finalizar\n")
    file_type = input()
    
    if file_type == "Finalizar":
        return "END" 
    else:
        return filesFolder + file_type

# função que termina a conexão cliente_udp
def finish_conection():
    finish = "END"
    cliente_udp.sendto(finish.encode(), server)
    cliente_udp.close()

def sync():
    global next_seq, rcv_base
    syn_and_next_seq = ('syn' +  str(next_seq).zfill(2)).encode()
    cliente_udp.sendto(syn_and_next_seq, server)
    print('syn enviado!')
    synack, _ = cliente_udp.recvfrom(BUFFER_SIZE)
    synack = synack.decode()
    if synack[:6] == 'synack':
        rcv_base = int(synack[6:9])
        print('sincronizado! (syn, synack)')
    print(rcv_base, 'rcv_base_sync')
    rcv_base = incrementa(rcv_base)
    print(rcv_base, 'rcv_base_sync')

def incrementa(val):
    return 1 - val

def snd_pkt(msg):
    global next_seq, rcv_base
    cliente_udp.sendto((str(next_seq).zfill(2) + str(rcv_base).zfill(2) + str(msg)).encode(), server)
    next_seq = incrementa(next_seq) 
    try:
        rcv_msg, _ = cliente_udp.recvfrom(BUFFER_SIZE)
    except socket.timeout:
        print('reenvia pacote!')
        rcv_msg, _ = cliente_udp.recvfrom(BUFFER_SIZE)

    rcv_msg = rcv_msg.decode()

    print(int(rcv_msg[:2]), rcv_base, '<- int(rcv_msg[:2]), rcv_base')
    if int(rcv_msg[:2]) == rcv_base: # next_seq(seq), rcv_base(ack)
        rcv_base = incrementa(rcv_base) 
        if snd_base == int(rcv_msg[2:4]):
            print('ack recebido:', snd_base)

def main(): 
    global next_seq, rcv_base
    
    # criação da pasta no cliente
    enderecoChegada = './clienteFile'

    if not os.path.exists(enderecoChegada):
        os.makedirs(enderecoChegada)

    filename = define_file()
    extensao = filename.split('.')[-1] # pegando extensão
    # enviando o syn, recebendo synack
    sync() 

    while True:

        # fim da conexão
        if filename == "END":
            finish_conection()
            break

        # enviando arquivo escolhido para o servidor
        with open(filename, 'rb') as f:
            extensao = filename.split('.')[-1] # pegando extensão (txt, pdf..)
            print('extensao:', extensao)
            snd_pkt(extensao)

            l = f.read(BUFFER_SIZE - 25) # lendo o primeiro pacotes de 1000 bytes
            # print(l)
            while l:
                snd_pkt(l.decode()) # enviando para a porta referenciada
                l = f.read(BUFFER_SIZE - 25) # ler os prox 1000 bytes do arq
                print(len(l), '<- len(l)')
            snd_pkt('') # arquivo vazio para indicar fim

            print("Arquivo " + filename + " enviado com sucesso.")
        f.close()

        # recebendo o arquivo que o servidor enviou
        extention, _ = cliente_udp.recvfrom(BUFFER_SIZE)
        extention = extention.decode('utf-8') 
        
        with open(f"{enderecoChegada}/arquivoNovo.{extention}", 'wb') as file: 
            while True:
                msg, servidor = cliente_udp.recvfrom(BUFFER_SIZE)
                if not msg:
                    break
                file.write(msg)
                file.flush()

            print("Arquivo " + enderecoChegada + "enviado com sucesso.")
        file.close()

        filename = define_file()
        
if __name__ == "__main__":
    main()  