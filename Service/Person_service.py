import sys

from Entity.Node import Node


class Person_service:
    def __init__(self, ip=None) -> None:
        self.node = Node(ip=sys.argv[1])

    def network_start(self):
        if not self.node._inicializado:
            self.node.sucessor = {"id": self.node.id, "ip": self.node.ip}
            self.node.antecessor = {"id": self.node.id, "ip": self.node.ip}
            self.node._inicializado = True
            print("Rede P2P Inicializada!")
        else:
            print("Erro: rede P2P já foi inicializada!")    