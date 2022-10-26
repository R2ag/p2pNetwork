class Node:
    def __init__(self, ip):
        self._inicializado = False
        self.ip = ip
        self.id = hash(ip)
        self.porta = 12345
        self.sucessor = {}
        self.antecessor = {}
