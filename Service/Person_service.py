from curses.has_key import has_key
import netifaces as ni
from Entity.Node import Node


class Person_service:
    def __init__(self, ip=None) -> None:
        self.node = Node(ip=self.get_ip())

    def get_ip(self):
        interfaces = ni.interfaces()
        for i in interfaces:
            ip = (ni.ifaddresses(i)[ni.AF_INET][0]['addr'])
            if ip != '127.0.0.1':    
                return ip

    def network_start(self):
        print("Criando nova Rede" )
        if not self.node._inicializado:
            self.node.sucessor = {"id": self.node.id, "ip": self.node.ip}
            self.node.antecessor = {"id": self.node.id, "ip": self.node.ip}
            self.node._inicializado = True
            print("Rede P2P Inicializada!")
        else:
            print("Erro: rede P2P já foi inicializada!")

        input("Pressione ENTER para continuar")    

    def network_lookup(self, node_id, node_ip):
        print("iniciando Lookup")
        pkg = {
            "codigo": 2,
            "identificador": self.node.id,
            "ip_origem_busca": node_ip,
            "id_busca": node_id
        }
        return pkg


    def lookup_received(self, msg):
        if (msg["id_busca"] > self.node.sucessor["id"] and self.node.sucessor["ip"] != self.node.ip and msg["identificador"] != self.node.sucessor["id"]):
            return(self.network_lookup(msg["id_busca"], msg["ip_origem_busca"]),self.node.sucessor["ip"])
        elif (msg["id_busca"] < self.node.antecessor["id"] and self.node.sucessor["ip"] != self.node.ip and msg["identificador"] != self.node.sucessor["id"]):
            return(self.network_lookup(msg["id_busca"], msg["ip_origem_busca"]), self.node.antecessor["ip"])
        else:
            pkg, ip = self.lookup_response(msg) 
            return(pkg, ip)


    def lookup_response(self, msg):
        pkg = {
            "codigo": 66,
            "id_busca": self.node.id,
            "id_origem": msg["id_busca"],
            "ip_origem": msg["ip_origem_busca"],
            "id_sucessor": self.node.sucessor["id"],
            "ip_sucessor": self.node.sucessor["ip"]
        }
        return pkg, msg["ip_origem_busca"]
    
    
    def network_join(self):
        pkg = {
            "codigo": 0,
            "id": self.node.id
        }
        return pkg

    def join_response(self):
        pkg = {
            "codigo": 64,
            "id_sucessor": self.node.id,
            "ip_sucessor": self.node.ip,
            "id_antecessor": self.node.antecessor["id"],
            "ip_antecessor": self.node.antecessor["ip"]
        }
        return pkg

    def network_init(self, msg):
        self.node.sucessor = {"id": msg["id_sucessor"], "ip": msg["ip_sucessor"]}
        self.node.antecessor = {"id": msg["id_antecessor"], "ip": msg["ip_antecessor"]}
        self.node._inicializado = True

    def update(self, opc):
        if opc == 0:
            pkg = {
                "codigo": 3,
                "identificador": self.node.id,
                "id_novo_sucessor": self.node.id,
                "ip_novo_sucessor": self.node.ip
            }
            return (pkg, self.node.antecessor["ip"])
        elif opc == 1:
            pkg = {
                "codigo": 3,
                "identificador": self.node.id,
                "id_novo_antecessor": self.node.id,
                "ip_novo_antecessor": self.node.ip
            }
            return (pkg, self.node.sucessor["ip"])

            

    def update_received(self, msg):
        if (msg.__contains__("id_novo_antecessor")):
            self.node.antecessor["id"] = msg["id_novo_antecessor"]
            self.node.antecessor["ip"] = msg["ip_novo_antecessor"]
            if (self.node.sucessor["ip"] == self.node.ip):
                self.node.sucessor["id"] = msg["id_novo_antecessor"]
                self.node.sucessor["ip"] = msg["ip_novo_antecessor"]
        elif (msg.__contains__("id_novo_sucessor")):
            self.node.sucessor["id"] = msg["id_novo_sucessor"]
            self.node.sucessor["ip"] = msg["ip_novo_sucessor"]
            if (self.node.antecessor["ip"] == self.node.ip):
                self.node.antecessor["id"] = msg["id_novo_sucessor"]
                self.node.antecessor["ip"] = msg["ip_novo_sucessor"]
        

        pkg = {
            "codigo": 67,
            "id_origem_mensagem": self.node.id 
        }

        return pkg

    def network_leave(self):
        pkg = {
            "codigo": 1,
            "identificador": self.node.id,
            "id_sucessor": self.node.sucessor["id"],
            "ip_sucessor": self.node.sucessor["ip"],
            "id_antecessor": self.node.antecessor["id"],
            "ip_antecessor": self.node.antecessor["ip"]
        } 

        return pkg

    def leave_update(self, msg):
        if (msg["identificador"] == self.node.antecessor["id"]):
            self.node.antecessor["id"] = msg["id_antecessor"]
            self.node.antecessor["ip"] = msg["ip_antecessor"]
        elif (msg["identificador"] == self.node.sucessor["id"]):
            self.node.sucessor["id"] = msg["id_sucessor"]
            self.node.sucessor["ip"] = msg["ip_sucessor"]
        
        pkg = {
            "codigo": 65,
            "identificador": self.node.id
        }
        return pkg

    def clear(self):
        self.node.sucessor = None
        self.node.antecessor = None