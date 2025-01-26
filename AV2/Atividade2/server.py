import socket
import threading
import json
import time
import queue

SERVER_HOST = '0.0.0.0'  
SERVER_PORT = 12345        
SYNC_INTERVAL = 30         

clients = []
clients_lock = threading.Lock()

message_queue = queue.Queue()

def handle_client(conn, addr):

    print(f"[+] Novo cliente conectado: {addr}")
    with clients_lock:
        clients.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break 
            try:
                message = json.loads(data.decode())
                message_queue.put((conn, message))
                print(f"Recebido de {addr}: {message}")
            except json.JSONDecodeError:
                print(f"Recebido dados inválidos de {addr}: {data}")
    except Exception as e:
        print(f"Erro com cliente {addr}: {e}")
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()
        print(f"[-] Cliente desconectado: {addr}")

def broadcast_message(message):
    with clients_lock:
        for client in clients:
            try:
                client.sendall(message.encode())
            except Exception as e:
                print(f"Erro ao enviar para cliente: {e}")

def synchronize_clocks():
    while True:
        time.sleep(SYNC_INTERVAL)
        with clients_lock:
            num_clients = len(clients)
        if num_clients == 0:
            print("[!] Nenhum cliente conectado para sincronização.")
            continue

        print("\n[+] Iniciando sincronização de relógios...")

        request = json.dumps({"type": "TIME_REQUEST"})
        broadcast_message(request)

        client_times = {}
        wait_time = 10
        start_time = time.time()

        while time.time() - start_time < wait_time and len(client_times) < num_clients:
            try:
                conn, message = message_queue.get(timeout=wait_time - (time.time() - start_time))
                if message.get("type") == "TIME":
                    client_times[conn] = message.get("time")
            except queue.Empty:
                break 

        if not client_times:
            print("[!] Nenhum horário recebido dos clientes.")
            continue

        average_time = sum(client_times.values()) / len(client_times)
        average_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(average_time))
        print(f"[*] Horários recebidos: {client_times}")
        print(f"[*] Horário médio calculado: {average_time_str}")

        adjustments = {}
        for client, c_time in client_times.items():
            adjustments[client] = average_time - c_time

        for client, adjust in adjustments.items():
            adjust_message = json.dumps({"type": "ADJUST", "adjust": adjust})
            try:
                client.sendall(adjust_message.encode())
            except Exception as e:
                print(f"Erro ao enviar ajuste para cliente: {e}")

        print("[*] Ajustes aplicados:")
        for client, adjust in adjustments.items():
            before = client_times.get(client, None)
            after = before + adjust if before else None
            try:
                client_addr = client.getpeername()
            except:
                client_addr = "Desconhecido"
            if before and after:
                before_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(before))
                after_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(after))
                print(f"    Cliente {client_addr}:")
                print(f"        Antes: {before_str}")
                print(f"        Depois: {after_str}")
                print(f"        Ajuste: {adjust:.2f} segundos")
        print("[+] Sincronização concluída.\n")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"[+] Servidor iniciado em {SERVER_HOST}:{SERVER_PORT}")
    print(f"[+] Aguardando conexões de clientes...")

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