# p2pNetwork
O trabalho consiste em aplicativo para uma rede P2P usando a linguagem Python com os métodos de entrada, atualização e saída da rede P2P.

Objetivos do trabalho:
Implementar um serviço de transferência de arquivos em redes P2P usando comunicação via sockets, conforme a especificação descrita neste documento;
Garantir a interoperabilidade das implementações conforme especificação.
Especificação:

UDP/ Porta 12345;
O identificador de cada nó da rede P2P será de 32 bits gerado aleatoriamente através do hash MD5 do endereço IP da máquina;
Funcionalidades previstas:
Join: permitir que uma nova máquina participe da rede;
Leave: permitir que uma máquina deixe a rede voluntariamente;
Lookup: permitir que se identifique o sucessor de um identificador na rede – na prática corresponde ao nó responsável pelo armazenamento do índice do conteúdo pesquisado;
Update: mensagem para atualização de sucessor;
Dados enviados/recebidos por funcionalidade:
Join:
Envia <código da mensagem, identificador da nova máquina>
Recebe <código da mensagem, identificador do novo sucessor, endereço IP do novo sucessor, identificador do novo antecessor, endereço IP do novo antecessor>
Leave:
Envia <código mensagem, identificador da máquina que está saindo, identificador do sucessor, endereço IP do sucessor, identificador do antecessor, endereço IP do antecessor
Recebe <código mensagem, identificador da origem (sucessor ou antecessor)>
Lookup:
Envia <código mensagem, identificador de origem da procura, endereço IP de origem da procura, identificador de quem esta procurando>
Recebe <código mensagem, identificador procurado, identificador do sucessor do id procurado, IP do sucessor do id procurado>
Update:

Envia <código da mensagem, identificador do novo sucessor, endereço
ip do novo sucessor>

Recebe <código da mensagem, identificador de origem> Formatação dos dados enviados/recebidos e formato dos pacotes:

Códigos de Mensagens: Inteiros de 8 bits (1 Byte).

0: Join

1: Leave

2: Lookup

3: Update

64: Resposta do Join

65: Resposta do Leave

66: Resposta do Lookup

67: Resposta do Update

Mensagens das Mensagens (JSON)
JOIN
ENVIO
{
   "codigo": int,
   "id": str
}
RESPOSTA
{
   "codigo": int,
   "id_sucessor": str,
   "ip_sucessor": str,
   "id_antecessor": str,
   "ip_antecessor": str
} 
LEAVE
ENVIO
{
   "codigo": int,
   "identificador", str,
   "id_sucessor": str,
   "ip_sucessor": str,
   "id_antecessor": str,
   "ip_antecessor": str
} 
RESPOSTA
{
   "codigo": int,
   "identificador": str,
} 
LOOKUP
ENVIO
{
   "codigo": int,
   "identificador": str,
   "ip_origem_busca": str,
   "id_busca": str,
} 
RESPOSTA
{
   "codigo": int,
   "id_busca": str,
   "id_origem": str,
   "ip_origem": str,
   "id_sucessor": str,
   "ip_sucessor": str
} 
UPDATE
ENVIO
ENVIO PARA O SUCESSOR
{
   "codigo": int,
   "identificador": str,
   "id_novo_sucessor": str,
   "ip_novo_sucessor": str
}
ENVIO PARA O ANTECESSOR
{
   "codigo": int,
   "identificador": str,
   "id_novo_antecessor": str,
   "ip_novo_antecessor": str
}
RESPOSTA
{
   "codigo": int,
   "id_origem_mensagem": str
} 
Operação

O programa deverá ter uma opção de inicialização da rede, onde o nó que cria essa rede é o único participante no momento da criação;
Para entrar na rede é preciso conhecer o endereço IP de alguém que esteja participando da rede, não necessariamente o nó criador;
Antes de enviar a mensagem de Join para juntar-se à rede, o nó que deseja participar da mesma precisa criar um identificador próprio e, através do seu contato na rede, fazer um Lookup pelo sucessor de id na rede. A reposta deste Lookup será o ponto de entrada de id na rede;
O nó que quer entrar na rede, após descobrir o sucessor do seu id, deverá enviar para este sucessor a mensagem de Join;
Após confirmado o Join, o nó id, que acabou de entrar na rede, precisa atualizar o seu antecessor e o seu sucessor através da mensagem de Update, informando-o que ele, id, é o seu novo sucessor/antecessor na rede;
Sempre que um nó for sair da rede ele precisa enviar uma mensagem de Leave aos seus vizinhos, sucessor e antecessor.
