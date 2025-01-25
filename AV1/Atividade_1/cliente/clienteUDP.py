import socket

TAMANHO_BLOCO = 1024

def iniciar_cliente():
    ip_servidor = input("Digite o endereço IP do servidor: ").strip()
    nome_arquivo = input("Digite o nome do arquivo a ser buscado: ").strip()
    novo_nome_arquivo = input("Digite o novo nome do arquivo: ").strip()
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cliente.sendto(nome_arquivo.encode('utf-8'), (ip_servidor, 5000))
        status, _ = cliente.recvfrom(TAMANHO_BLOCO)
        status = status.decode('utf-8')
        if status == "EXISTE":
            tamanho, _ = cliente.recvfrom(TAMANHO_BLOCO)
            tamanho = int(tamanho.decode('utf-8'))
            recebido = 0
            with open(novo_nome_arquivo, 'wb') as arquivo:
                while recebido < tamanho:
                    dados, _ = cliente.recvfrom(TAMANHO_BLOCO)
                    arquivo.write(dados)
                    recebido += len(dados)
            print(f"Arquivo recebido e salvo como '{novo_nome_arquivo}'.")
        else:
            with open(novo_nome_arquivo, 'w') as arquivo:
                arquivo.write("Vazio")
            print(f"Arquivo não encontrado no servidor. '{novo_nome_arquivo}' criado com conteúdo 'Vazio'.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        cliente.close()

if __name__ == "__main__":
    iniciar_cliente()