import socket
import threading
import os

HOST = 'localhost'
PORTA = 5000
TAMANHO_BLOCO = 1024

def lidar_com_cliente(conexao, endereco):
    try:
        print(f"Conexão estabelecida com {endereco}")
        nome_arquivo = conexao.recv(TAMANHO_BLOCO).decode('utf-8')
        if not nome_arquivo:
            conexao.close()
            return
        if os.path.isfile(nome_arquivo):
            conexao.sendall("EXISTE".encode('utf-8'))
            with open(nome_arquivo, 'rb') as arquivo:
                while True:
                    dados = arquivo.read(TAMANHO_BLOCO)
                    if not dados:
                        break
                    conexao.sendall(dados)
        else:
            conexao.sendall("NAO_EXISTE".encode('utf-8'))
    except Exception as e:
        print(f"Erro com {endereco}: {e}")
    finally:
        conexao.close()
        print(f"Conexão encerrada com {endereco}")

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORTA))
    servidor.listen(5)
    print(f"Servidor executando em {HOST}:{PORTA}")
    while True:
        conexao, endereco = servidor.accept()
        threading.Thread(target=lidar_com_cliente, args=(conexao, endereco)).start()

if __name__ == "__main__":
    iniciar_servidor()