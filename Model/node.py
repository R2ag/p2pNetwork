class Node:
    def __init__(self, ip):
        self._inicializado = False
        self.ip = ip
        self.id = hash(f"{ip}")
        self.porta = 12345
        self.sucessor = {}
        self.antecessor = {}

    def network_start(self):
        if not self.node._inicializado:
            self.node.sucessor = {"id": self.node.id, "ip": self.node.ip}
            self.node.antecessor = {"id": self.node.id, "ip": self.node.ip}
            self.node._inicializado = True
            return 1
        else:
            return 2
            
    def network_leave(self):
        pass