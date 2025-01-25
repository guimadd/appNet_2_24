import socket
import threading
import json
import time

# Configurações do servidor
SERVER_HOST = '0.0.0.0'  # Escuta em todas as interfaces
SERVER_PORT = 12345        # Porta para conexões
SYNC_INTERVAL = 30         # Intervalo de sincronização em segundos

# Lista para armazenar conexões dos clientes
clients = []
clients_lock = threading.Lock()

def handle_client(conn, addr):
    """
    Thread para lidar com a comunicação com um cliente.
    """
    print(f"[+] Novo cliente conectado: {addr}")
    with clients_lock:
        clients.append(conn)
    try:
        while True:
            # Mantém a conexão aberta
            data = conn.recv(1024)
            if not data:
                break
            # Aqui, poderíamos processar mensagens adicionais do cliente se necessário
    except:
        pass
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()
        print(f"[-] Cliente desconectado: {addr}")

def broadcast_message(message):
    """
    Envia uma mensagem para todos os clientes conectados.
    """
    with clients_lock:
        for client in clients:
            try:
                client.sendall(message.encode())
            except:
                pass  # Se ocorrer erro, ignore e prossiga

def synchronize_clocks():
    """
    Realiza a sincronização dos relógios dos clientes.
    """
    while True:
        time.sleep(SYNC_INTERVAL)
        if not clients:
            print("[!] Nenhum cliente conectado para sincronização.")
            continue

        print("\n[+] Iniciando sincronização de relógios...")

        # Solicita o horário atual de todos os clientes
        request = json.dumps({"type": "TIME_REQUEST"})
        broadcast_message(request)

        # Dicionário para armazenar horários dos clientes
        client_times = {}
        threads = []

        def receive_time(client_conn):
            """
            Recebe o horário de um cliente.
            """
            try:
                data = client_conn.recv(1024)
                if data:
                    message = json.loads(data.decode())
                    if message["type"] == "TIME":
                        client_times[client_conn] = message["time"]
            except:
                pass

        # Inicia threads para receber os horários dos clientes
        with clients_lock:
            for client in clients:
                thread = threading.Thread(target=receive_time, args=(client,))
                thread.start()
                threads.append(thread)

        # Aguarda um curto período para receber respostas
        time.sleep(5)

        # Aguarda todas as threads finalizarem
        for thread in threads:
            thread.join()

        if not client_times:
            print("[!] Nenhum horário recebido dos clientes.")
            continue

        # Calcula o horário médio
        average_time = sum(client_times.values()) / len(client_times)
        print(f"[*] Horários recebidos: {client_times}")
        print(f"[*] Horário médio calculado: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(average_time))}")

        # Calcula os ajustes para cada cliente
        adjustments = {}
        for client, c_time in client_times.items():
            adjustments[client] = average_time - c_time

        # Envia os ajustes para os clientes
        for client, adjust in adjustments.items():
            adjust_message = json.dumps({"type": "ADJUST", "adjust": adjust})
            try:
                client.sendall(adjust_message.encode())
            except:
                pass

        # Exibe os ajustes e os horários antes/depois
        print("[*] Ajustes aplicados:")
        for client, adjust in adjustments.items():
            before = client_times.get(client, None)
            after = before + adjust if before else None
            client_addr = client.getpeername()
            if before and after:
                print(f"    Cliente {client_addr}:")
                print(f"        Antes: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(before))}")
                print(f"        Depois: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(after))}")
                print(f"        Ajuste: {adjust:.2f} segundos")
        print("[+] Sincronização concluída.\n")

def start_server():
    """
    Inicia o servidor e aceita conexões de clientes.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"[+] Servidor iniciado em {SERVER_HOST}:{SERVER_PORT}")
    print(f"[+] Aguardando conexões de clientes...")

    # Inicia a thread de sincronização
    sync_thread = threading.Thread(target=synchronize_clocks, daemon=True)
    sync_thread.start()

    try:
        while True:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[!] Servidor encerrado.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
