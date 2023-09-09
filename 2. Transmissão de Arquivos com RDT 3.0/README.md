# Entrega 2 - Infracom

Este projeto simula um sistema com execução de envio e recuperação de arquivos entre o cliente e o servidor por meio de uma transmissão confiável baseada em UDP com aplicação do canal RDT3.0 e implementação de um gerador de perda de pacotes aleatórios, para simular um ambiente de transmissão de pacotes real e demonstrar a eficiência do RDT3.0 na ocasião. Para tal finalidade, utilizamos as bibliotecas `socket` e `os` da linguagem Python para a abertura da conexão entre o processo cliente e o processo servidor e manuseio do caminho de acesso dos arquivos, respectivamente.

## Especificações do Projeto

- O funcionamento do projeto exige que os programas `cliente.py` e `servidor.py` sejam executados em terminais separados. O usuário deve primeiro executar o programa servidor em um terminal, usando `python servidor.py`, e, em seguida, executar o programa cliente no outro terminal, usando `python cliente.py`.
- Internamente, o programa apresenta uma interface para que o usuário selecione o arquivo para transferência ou  encerre a execução dos processos. Um arquivo `.txt` é disponibilizado para testagem do programa no diretório `files`.
-  Os programas devem ser mantidos paralelamente em execução e encerrados de maneira apropriada por meio da interface interna apresentada no código.

## Equipe
Bianca Duarte Silva (bds) \
Caio Henrique Araújo Braga (chab) \
Edson José Araújo Pereira Júnior (ejapj) \
Kaylane Gonçalves Lira (kgl) \
Rafael da Silva Barros (rsb7) \
Yasmim Vitória Silva de Oliveira (yvso)
