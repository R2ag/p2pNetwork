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
        self.t1.start()
        self.t2.start()
        

    #Interface de interação do programa com o usuário
    def interface(self) -> None:
        while True:
            os.system("clear")
            print("######################################")
            print("# 1 - Criar uma nova rede P2P        #")
            print("# 2 - Entrar em uma rede P2P         #")
            print("# 3 - Sair da rede P2P               #")
            print("# 4 - Imprimir informacoes do no     #")
            print("# 9 - Sair do programa               #")
            print("######################################")
            try:
                opc = int(input("=> "))
                if opc == 1:
                    self.network_start()
                elif opc == 2:
                    self.network_login(self.person_service.node.id, self.person_service.node.ip)
                elif opc == 3:
                    self.network_leave()
                elif opc == 4:
                    self.node_info()
                elif opc == 9:
                    if self.person_service.node._inicializado:
                        self.network_leave()
                    os._exit(0)
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
                self.join_response(cliente[0])
            elif string_dict["codigo"] == 1:
                self.leave_update(string_dict, cliente[0])
            elif string_dict["codigo"] == 2:
                self.lookup_received(string_dict)
            elif string_dict["codigo"] == 3:
                self.update_received(string_dict, cliente[0])
            elif string_dict["codigo"] == 64:
                self.network_init(string_dict)
            elif string_dict["codigo"] == 65:
                print("leave ok")
                self.clear()
            elif string_dict["codigo"] == 66:
                self.network_join(cliente[0])
            elif string_dict["codigo"] == 67:
                print("update ok")

    
    #Função responsável por enviar os pacotes aos destinatários na rede.
    def send(self, msg, ip):
        print(f"enviando mensagem para {ip}")
        dest = (ip, 12345)
        try:
            msg_json = json.dumps(msg)
            self.udp.sendto(msg_json.encode('utf-8'), dest)
        except Exception as ex:
            print("Erro de Conexão")
            sys.exit(0)

    def clear(self):
        self.person_service.clear()
    
    def network_start(self):
        self.person_service.network_start()

    def network_login(self, node_id, node_ip):
        os.system("clear")
        print("Iniciando conexao com a rede!")
        ip_dest = input("Informe o IP do no: ")
        self.send(self.person_service.network_lookup(node_id, node_ip), ip_dest)

    def lookup_received(self, msg):
        print("Recebida mensagem de lookup")
        pkg, ip = self.person_service.lookup_received(msg)
        self.send(pkg, ip)
   
    def network_join(self, ip):
        self.send(self.person_service.network_join(), ip)

    def join_response(self, ip):
        self.send(self.person_service.join_response(), ip)
        
    def network_init(self, msg):
        self.person_service.network_init(msg)
        for i in range(2):
            pkg, ip = self.person_service.update(i)
            self.send(pkg, ip)

    def update_received(self, msg, cliente):
        self.send(self.person_service.update_received(msg), cliente)

    def node_info(self):
        os.system("clear")
        print("#      Informacoes do No       #")
        print(f"# ID: {self.person_service.node.id}")
        print(f"# IP: {self.person_service.node.ip}")
        print(f"# Sucessor: {self.person_service.node.sucessor}")
        print(f"# Antecessor: {self.person_service.node.antecessor}")
        print("#------------------------------#")
        input("Pressione ENTER para continuar")

    def network_leave(self):
        pkg = self.person_service.network_leave()
        self.send(pkg, self.person_service.node.antecessor["ip"])
        self.send(pkg, self.person_service.node.sucessor["ip"])

    def leave_update(self, msg, ip):
        self.send(self.person_service.leave_update(msg), ip)