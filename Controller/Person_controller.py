from cgitb import lookup
import json
import os
import socket
import sys
import threading
from Service.Person_service import Person_service


class Person_controller:
    def __init__(self):
        self.person_service = Person_service()
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.t1 = threading.Thread(target=self.receiver)
        self.t2 = threading.Thread(target=self.interface)

    #Interface de interação do programa com o usuário
    def interface(self) -> None:
        while True:
            os.system("clear")
            print("######################################")
            print("# 1 - Criar uma nova rede P2P        #")
            print("# 2 - Entrar em uma rede P2P         #")
            print("# 3 - Sair da rede P2P               #")
            print("# 4 - Imprimir informações do nó     #")
            print("# 9 - Sair do programa               #")
            print("######################################")
            try:
                opc = int(input("=> "))
                if opc == 1:
                    self.network_start()
                elif opc == 2:
                    self.netwok_lookup(self.person_service.node.id, self.person_service.node.ip)
                elif opc == 3:
                    self.network_leave()
                elif opc == 4:
                    self.node_info()
                elif opc == 9:
                    self.__t1.terminate()
                    sys.exit(0)
            except ValueError:
                opc = 0



    #Função responsável por receber as mensagens da rede.
    def receiver(self) -> None:
        print(f"=> Iniciando P2P Server")
        orig = ("", 12345)
        self.udp.bind(orig)

        while True:
            msg, cliente = self.udp.recvfrom(1024)
            msg_decoded = msg.decode("utf-8")
            string_dict = json.loads(msg_decoded)
            if string_dict["codigo"] == 0:
                self.join_response(cliente)
            elif string_dict["codigo"] == 1:
                pass
            elif string_dict["codigo"] == 2:
                self.lookup_received(string_dict)
            elif string_dict["codigo"] == 3:
                pass
            elif string_dict["codigo"] == 64:
                pass
            elif string_dict["codigo"] == 65:
                pass
            elif string_dict["codigo"] == 66:
                self.network_join(string_dict["ip"])
            elif string_dict["codigo"] == 67:
                pass

    
    #Função responsável por enviar os pacotes aos destinatários na rede.
    def send(self, msg, ip):
        dest = (ip, 12345)
        try:
            msg_json = json.dumps(msg)
            self.udp.sendto(msg_json.encode('utf-8'), dest)
        except Exception as ex:
            print("Erro de Conexão")
            sys.exit(0)

    
    def network_start(self):
        self.person_service.network_start()

    def netwok_lookup(self, node_id, node_ip):
        os.system("clear")
        ip_dest = input("Informe o IP do nó: ")
        self.send(self.person_service.network_lookup(node_id, node_ip, ip_dest))

    def lookup_received(self, msg):
        self.send(self.person_service.lookup_received(msg))

    def network_join(self, ip):
        self.send(self.person_service.network_join(ip))

    def join_response(self, ip):
        self.send(self.person_service.join_response(ip))
        
           
