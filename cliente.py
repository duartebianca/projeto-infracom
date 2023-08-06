import socket
import os
from socket import socket as funcSocket

buffer_size  = 1024

HOST = 'localhost'
PORT = 5000
dest = (HOST, PORT)

udp = funcSocket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('localhost',3000))

def define_file():
    print("Que tipo de arquivo deseja receber?\n")
    print("(1) PDF\n(2)TXT\n(3) MP4\n(4) MP3\n(5) *IMG\n(6) Desejo encerrar conexao\n")
    file_type = input()
    
    if file_type == '1':  # Adicionei int() aqui para converter a entrada para inteiro
        return "testePDF.pdf"
    elif file_type == '2':
        return "testeTXT.txt"
    elif file_type == '3':
        return "testeMP4.mp4"
    elif file_type == '4':
        return "testeMP3.ogg"
    elif file_type == '5':
        return "testeIMG.jpeg"
    else:
        return "END" 
    
def finish_conection():
    finish = "END"
    udp.sendto(finish.encode(),dest)
    print("oi")
    udp.close()


def main(): 
    enderecoChegada = './clienteFile'

    if not os.path.exists(enderecoChegada):
        os.makedirs(enderecoChegada)


    # enderecoEnvio = str(input())
    enderecoEnvio = define_file()

    while True:
        #enderecoEnvio = './arquivos/teste.mp4'

        if enderecoEnvio == "END":
            finish_conection()

        # print(enderecoEnvio)

        with open(enderecoEnvio, 'rb') as f:
            extensao = enderecoEnvio.split('.')[-1] # pegando extensão
            udp.sendto(extensao.encode(), dest) # envio da string codificada
            l = f.read(buffer_size) # lendo o primeiro pacotes de 1024 bytes
            while l:
                #print(l)
                udp.sendto(l, dest) # enviando para a porta referenciada
                l = f.read(buffer_size) # ler os prox 1024 bytes do arq
            udp.sendto(b'', dest) # arquivo vazio para indicar fim
        f.close()
        
        extention, servidor = udp.recvfrom(buffer_size)

        with open(f"{enderecoChegada}/arquivoNovo.{extention.decode()}", 'wb') as file: 
            while True:
                msg, servidor = udp.recvfrom(buffer_size)
                if not msg:
                    break
                # print(msg)
                file.write(msg)
                file.flush()
        file.close()

        enderecoEnvio = define_file()
        
if __name__ == "__main__":
    main()  
# udp.sendto(enderecoEnvio.encode(), dest)
