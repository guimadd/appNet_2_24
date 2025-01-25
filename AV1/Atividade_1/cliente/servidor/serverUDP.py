import socket
import os
import threading

HOST = 'localhost'
PORTA = 5000
TAMANHO_BLOCO = 1024

def lidar_requisicao(nome_arquivo, endereco, servidor):
    if os.path.isfile(nome_arquivo):
        servidor.sendto("EXISTE".encode('utf-8'), endereco)
        tamanho = os.path.getsize(nome_arquivo)
        servidor.sendto(str(tamanho).encode('utf-8'), endereco)
        with open(nome_arquivo, 'rb') as arquivo:
            while True:
                bloco = arquivo.read(TAMANHO_BLOCO)
                if not bloco:
                    break
                servidor.sendto(bloco, endereco)
    else:
        servidor.sendto("NAO_EXISTE".encode('utf-8'), endereco)

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORTA))
    print(f"Servidor UDP executando em {HOST}:{PORTA}")
    while True:
        try:
            dados, endereco = servidor.recvfrom(TAMANHO_BLOCO)
            nome_arquivo = dados.decode('utf-8')
            if not nome_arquivo:
                continue
            threading.Thread(target=lidar_requisicao, args=(nome_arquivo, endereco, servidor)).start()
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    iniciar_servidor()
