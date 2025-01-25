import socket

TAMANHO_BLOCO = 1024

def iniciar_cliente():
    ip_servidor = input("Digite o endereço IP do servidor: ").strip()
    nome_arquivo = input("Digite o nome do arquivo a ser buscado: ").strip()
    novo_nome_arquivo = input("Digite o novo nome do arquivo: ").strip()
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((ip_servidor, 5000))
        cliente.sendall(nome_arquivo.encode('utf-8'))
        status = cliente.recv(TAMANHO_BLOCO).decode('utf-8')
        if status == "EXISTE":
            with open(novo_nome_arquivo, 'wb') as arquivo:
                while True:
                    dados = cliente.recv(TAMANHO_BLOCO)
                    if not dados:
                        break
                    arquivo.write(dados)
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
