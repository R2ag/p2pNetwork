import os

class interface:
    def main_menu():
        os.system("clear")
        print("######################################")
        print("# 1 - Criar uma nova rede P2P        #")
        print("# 2 - Entrar em uma rede P2P         #")
        print("# 3 - Sair da rede P2P               #")
        print("# 4 - Imprimir informações do nó     #")
        print("# 9 - Sair do programa               #")
        print("######################################")

        return int(input("->"))

    def node_info(node):
        os.system("clear")
        print("#      Informações do Nó       #")
        print(f"# ID: {node.id}")
        print(f"# IP: {node.ip}")
        print(f"# Sucessor: {node.sucessor}")
        print(f"# Antecessor: {node.antecessor}")
        print("#------------------------------#")
        input("Pressione ENTER para continuar")

    def join_network():
        os.system("clear")
        ip = input("Informe o IP do nó: ")
        print("Conectando...")
        return ip

    def msg_status(status_code):
        if(status_code == 11):
            print("Rede P2P Inicializada!")
        elif(status_code == 12):
            print("Erro: rede P2P já foi inicializada!")

