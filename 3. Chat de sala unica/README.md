# Entrega 3 - Infracom

Este projeto consiste na implementação de um chat de sala única com o paradigma cliente-servidor. O chat será exibido por linha de comando e utilizará uma transmissão confiável baseada no protocolo RDT 3.0. O objetivo é permitir a comunicação simultânea de vários clientes em uma sala de chat, onde as mensagens serão formatadas e exibidas de acordo com um padrão específico.

## Funcionamento do Programa

- O funcionamento do projeto exige que os programas `cliente.py` e `servidor.py` sejam executados em terminais separados. O usuário deve primeiro executar o programa servidor em um terminal, usando `python servidor.py`, e, em seguida, executar o programa cliente no outro terminal, usando `python cliente.py`.
- Há suporte para execução simultânea de até 3 terminais de clientes (utilização de 3 portas) no projeto. A execução dos programas clientes requisitam do usuário um nome de login inicial que não possui relação com a sala de chat. Este user inicial serve apenas para designar o número da porta correspondente àquele cliente, o qual deve ser selecionado dentre as opções fornecidas no arquivo `users.txt`. Vale salientar, que é permitindo na primeira tentativa de login ,"hi, meu nome eh  ", que o usuário utilize outro nome distinto para acessar a sala de chat, todavia após logar com o nome informdo, será negado qualquer tentativa de login com outro nome pelo usuário.
- Internamente, é apresentada no chat uma interface para que o usuário visualize os comandos nativos do programa. Os comandos reconhecidos são:
  - `hi, meu nome eh <nome_do_usuario>`: conectar-se à sala.
  - `bye`: desconectar-se da sala.
  - `list`: exibir a lista de usuários do chat.
  - `mylist`: exibir lista de amigos.
  - `addtomylist <nome_do_usuario>`: adicionar usuário à lista de amigos.
  - `rmvfrommylist <nome_do_usuario>`: remover usuário da lista de amigos.
  - `ban <nome_do_usuario>`: banir usuário da sala.
- As mensagens enviadas no chat obedecem o modelo `<IP>:<PORTA>/~<nome_usuario>: <mensagem> <hora-data>`

## Especificações do Projeto

- Quando um novo usuário se conecta à sala de chat, todos os usuários logados na sala são notificados.
- Toda mensagem enviada por um usuário conectado é exibida para os outros usuários.
- Dois usuários não podem se conectar simultaneamente à sala utilizando o mesmo nome.
- Ao adicionar um usuário à lista de amigos, ele ganhará uma tag de `[Amigo]` ao lado do nome nas mensagens subsequentes. Ao remover um usuário da lista de amigos, essa tag será removida.
- Ao banir um usuário da sala, o servidor iniciará uma contagem. Se essa contagem atingir metade ou mais clientes conectados, o usuário mencionado será banido. Além disso, todos os usuários receberão uma mensagem de aviso no chat informando o número de votos e a quantidade necessária para que o usuário seja removido do servidor.
- Os programas devem ser mantidos paralelamente em execução e encerrados de maneira apropriada por meio dos comandos internos apresentados no código.

## Equipe
Bianca Duarte Silva (bds) \
Caio Henrique Araújo Braga (chab) \
Edson José Araújo Pereira Júnior (ejapj) \
Kaylane Gonçalves Lira (kgl) \
Rafael da Silva Barros (rsb7) \
Yasmim Vitória Silva de Oliveira (yvso)
