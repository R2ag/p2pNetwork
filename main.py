#!/usr/sbin/python3
# -*- coding: utf-8 -*-
import socket
import multiprocessing as mp
import json
import sys
import os


class Node:
    def __init__(self, ip):
        self._inicializado = False
        self.ip = ip
        self.id = hash(ip)
        self.porta = 12345
        self.sucessor = {}
        self.antecessor = {}


class Controller:
    def __init__(self, ip=None) -> None:
        self.node = Node(ip=sys.argv[1])
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__t1 = mp.Process(target=self.controle)
        self.__t1.start()
        self.interface()



    #Função responsável por receber os pacotes da rede.
    def receiver(self) -> None:
        print(f"=> Iniciando P2P Server (ip={self.node.ip}, porta={self.node.porta})")
        orig = ("", self.node.porta)
        self.udp.bind(orig)

        while True:
            msg, cliente = self.udp.recvfrom(1024)
            msg_decoded = msg.decode("utf-8")
            string_dict = json.loads(msg_decoded)
            if string_dict["codigo"] == 0:
                pass
            elif string_dict["codigo"] == 1:
                pass
            elif string_dict["codigo"] == 2:
                pass
            elif string_dict["codigo"] == 3:
                pass
            elif string_dict["codigo"] == 64:
                pass
            elif string_dict["codigo"] == 65:
                pass
            elif string_dict["codigo"] == 66:
                pass
            elif string_dict["codigo"] == 67:
                pass

    
    #Função responsável por enviar os pacotes aos destinatários na rede.
    def send(self, msg, ip):
        dest = [ip, 12345]
        try:
            msg_json = json.dumps(msg)
            self.udp.sendto(msg_json.encode('utf-8'), dest)
        except Exception as ex:
            print("Erro de Conexão")
            sys.exit(0)

    
    #Interface de controle do programa
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
                    self.network_lookup()
                elif opc == 3:
                    self.network_leave()
                elif opc == 4:
                    self.node_info()
                elif opc == 9:
                    self.__t1.terminate()
                    sys.exit(0)
            except ValueError:
                opc = 0


    #Função de inicialização da rede
    def network_start(self):
        if not self.node._inicializado:
            self.node.sucessor = {"id": self.node.id, "ip": self.node.ip}
            self.node.antecessor = {"id": self.node.id, "ip": self.node.ip}
            self.node._inicializado = True
            print("Rede P2P Inicializada!")
        else:
            print("Erro: rede P2P já foi inicializada!")

    #Função responsável por encontrar a posição do nó ingressante na rede
    def network_lookup(self):
        os.system("clear")
        ip = input("Informe o IP do nó: ")
        pkg = {
            "codigo": 2,
            "identificador": self.node.id,
            "ip_origem_busca": self.node.ip,
            "id_busca": str ###Quem é esse? Identificar esse sujeito para poder rodar o código!
        }
        self.send(pkg, ip)
        input("Pressione ENTER para continuar")

    #função responsável por ingressar o nó na rede
    def network_join(self, ip):
        pkg = {
            "codigo": 0,
            "id": self.node.id
        }
        self.send(pkg, ip)
        input("Pressione ENTER para continuar")

    def network_leave(self):
        pass

    
    def node_info(self):
        os.system("clear")
        print("#      Informações do Nó       #")
        print(f"# ID: {self.node.id}")
        print(f"# IP: {self.node.ip}")
        print(f"# Sucessor: {self.node.sucessor}")
        print(f"# Antecessor: {self.node.antecessor}")
        print("#------------------------------#")
        input("Pressione ENTER para continuar")



if __name__ == "__main__":
    if len(sys.argv) == 2:
        controll = Controller(ip=sys.argv[1])
    else:
        print("Modo de utilização: python3 main.py <ENDEREÇO_IP>")
        sys.exit(0)


# XGH - Vai Cavalo!!!