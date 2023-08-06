# Projeto - Infracom

Este projeto simula um sistema com execução de envio e recuperação de arquivos entre o cliente e o servidor por meio de uma conexão UDP. Para tal finalidade, utilizamos as bibliotecas `socket` e `os` da linguagem Python para a abertura da conexão entre o processo cliente e o processo servidor e manuseio do caminho de acesso dos arquivos, respectivamente.

## Especificações do Projeto

- O funcionamento do projeto exige que os programas `cliente.py` e `servidor.py` sejam executados em terminais separados. O usuário deve primeiro executar o programa servidor em um terminal, usando `python servidor.py`, e, em seguida, executar o programa cliente no outro terminal, usando `python cliente.py`.
- Internamente, o programa apresenta uma interface para que o usuário selecione o arquivo que deseja transferir ou  encerre a execução dos processos. Quatro arquivos são disponibilizados no diretório `files` para testagem do programa, com extensões `.jpeg`, `.mp3`, `.pdf` e `.txt`.
- Os programas devem ser mantidos paralelamente em execução e encerrados de maneira apropriada por meio da interface interna apresentada no código. 

### Equipe
Bianca Duarte Silva (bds) \
Caio Henrique Araújo Braga (chab) \
Edson José Araújo Pereira Júnior (ejapj) \
Kaylane Gonçalves Lira (kgl) \
Rafael da Silva Barros (rsb7) \
Yasmim Vitória Silva de Oliveira (yvso)
