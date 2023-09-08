import socket
import os
import random
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
tentativas = 10

# criando socket cliente_udp
cliente_udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
cliente_udp.bind((HOST ,3000))

# função que pega o input do user e define o arquivo desejado
def define_file():
    print("----------------------------------------------------------")
    print("Escreva o nome do arquivo que quer receber:\n")
    print("Opções disponíveis:")
    print("- testePDF.pdf")
    print("- testeTXT.txt")
    print("- testeMP3.mp3")
    print("- testeIMG.jpeg\n")
    print("Ou finalize a conexão com")
    print("- Finalizar\n")
    file_type = input()
    
    return file_type

# função que termina a conexão cliente_udp
def finish_conection():
    finish = "fyn"
    snd_pkt(finish)
    fynack = rcv_pkt()
    if fynack == 'fynack':
        cliente_udp.close()
    else:
        finish_conection

def error_gen():
    numero_aleatorio = random.random()
    probabilidade_de_erro = 0.5
    if numero_aleatorio < probabilidade_de_erro:
        return 1
    else: 
        return 0

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
    if error_gen() == 0:
        cliente_udp.sendto((str(next_seq).zfill(2) + str(rcv_base).zfill(2) + str(msg)).encode(), server)
    next_seq_antigo = next_seq
    next_seq = incrementa(next_seq) 

    for i in range(tentativas):
        flag = 0
        flag_erro = 0
        try:
            rcv_msg, _ = cliente_udp.recvfrom(BUFFER_SIZE)    
            flag = 1
        except socket.timeout:
            if i == (tentativas - 1): 
                flag_erro = 1
                break 
            print('Erro no envio, reenvia pacote!')
            if error_gen() == 0:
                cliente_udp.sendto((str(next_seq_antigo).zfill(2) + str(rcv_base).zfill(2) + str(msg)).encode(), server)
        if flag == 1:
            break
    if flag_erro == 1:
        print(f"Falha no envio! Não foi possivel enviar pacote {tentativas}x seguidas.")
        return 1
    rcv_msg = rcv_msg.decode()

    # print('(ACK recebido)', int(rcv_msg[:2]), '==', rcv_base, 'rcv_base (client)')
    if int(rcv_msg[:2]) == rcv_base: # next_seq (server) - seq = rcv_base (cliente) 
        rcv_base = incrementa(rcv_base) 
        if int(rcv_msg[2:4]) == snd_base: 
            print('Pacote enviado, ACK recebido!')
    # rcv_base (server) - ack = snd_base (cliente)
    # snd_base (ack recebido), next_seq (soma de tamanho enviado), rcv_base (soma de tamanho recebido)

def rcv_pkt():
    global rcv_base, snd_base, next_seq
    msg, cliente = cliente_udp.recvfrom(BUFFER_SIZE)
    msg = msg.decode()
    if int(msg[:2]) == rcv_base: 
        rcv_base = incrementa(rcv_base)
    cliente_udp.sendto((str(next_seq).zfill(2) + str(rcv_base).zfill(2)).encode(), cliente)
    
    # print(next_seq, rcv_base, '<- next_seq, rcv_base (cliente)')
    next_seq = incrementa(next_seq)
    # print(msg[4:])
    return str(msg[4:]) 

def main(): 
    global next_seq, rcv_base
    
    # criação da pasta no cliente
    enderecoChegada = './clienteFile'

    if not os.path.exists(enderecoChegada):
        os.makedirs(enderecoChegada)

    # pegando caminho da pasta de arquivos
    pasta = "files"
    caminho_pasta = os.path.join(os.path.dirname(__file__), pasta)

    arquivo = define_file()
    extensao = arquivo.split('.')[-1] # pegando extensão
    print(extensao, 'extensao -')

    # enviando o syn, recebendo synack
    sync() 

    while True:

        # fim da conexão
        if arquivo == "Finalizar":
            finish_conection()
            break

        enderecoEnvio = os.path.join(caminho_pasta, arquivo)

        # Verifica se o arquivo existe
        if not os.path.exists(enderecoEnvio):
            print("----------------------------------------------------------")
            print(f"Arquivo '{arquivo}' não encontrado. Tente novamente.\n")
            continue

        extensao = enderecoEnvio.split('.')[-1] # pegando extensão (txt, pdf..)
        print(extensao, 'extensao --')

        # enviando arquivo escolhido para o servidor
        cliente_udp.settimeout(2)
        # print(enderecoEnvio)
        with open(enderecoEnvio, 'rb') as f:
            snd_pkt(extensao)

            l = f.read(BUFFER_SIZE - 25) # lendo o primeiro pacotes de 1000 bytes
            while l:
                snd_pkt(l.decode()) # enviando para a porta referenciada
                l = f.read(BUFFER_SIZE - 25) # ler os prox 1000 bytes do arq
                # print(len(l), '<- len(l)')
            snd_pkt('') # arquivo vazio para indicar fim
            print("Arquivo " + arquivo + " enviado com sucesso.")
        f.close()

        cliente_udp.settimeout(None)

        # recebendo o arquivo que o servidor enviou
        extention = rcv_pkt()

        with open(f"{enderecoChegada}/arquivoNovo.{extention}", 'wb') as f: 
            while True:
                msg = rcv_pkt()
                if not msg:
                    break
                f.write(msg.encode())
                f.flush()
            f.close()
        print(f"Arquivo {enderecoChegada}/arquivoNovo.{extention} recebido de volta!")

        arquivo = define_file()
        
if __name__ == "__main__":
    main()  