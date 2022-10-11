import json
from platform import node
import socket
import sys
import multiprocessing as mp
from Model.node import Node
from View.interface import interface

class p2p_controller:
    def __init__(self, ip=None) -> None:
        self.node = Node(ip=sys.argv[1])
        self.view = interface()
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__t1 = mp.Process(target=self.controle)
        self.__t1.start()
   
    def main_controll(self):
        try:
            opc = self.view.main_menu()
            if opc == 1:
                status = 10+self.node.network_start()
                self.view.msg_status(status)

            elif opc == 2:
                ip = self.view.join_network()
                status = 20+self.join_network(ip)
                self.view.msg_status(status)
            elif opc == 3:
                status = 30+self.node.network_leave()
                self.view.msg_status(status)
            elif opc == 4:
                self.view.node_info(self.node)
            elif opc == 9:
                self.__t1.terminate()
                sys.exit(0)
        except ValueError:
            opc = 0
    
    def join_network(ip):
        pass
    
    def controll_receiver(self) -> None:
        
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

