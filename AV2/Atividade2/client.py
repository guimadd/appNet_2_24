import socket
import threading
import json
import time
import sys

# Configurações do cliente
SERVER_HOST = 'localhost'  # Endereço do servidor (ajuste conforme necessário)
SERVER_PORT = 12345        # Porta do servidor
OFFSET = 5                 # Deslocamento inicial em segundos (positivo ou negativo)

class ClientClock:
    """
    Classe para simular o relógio do cliente.
    """
    def __init__(self, offset=0):
        self.lock = threading.Lock()
        self.offset = offset
        self.running = True

    def get_time(self):
        """
        Retorna o horário atual do cliente com o deslocamento.
        """
        with self.lock:
            return time.time() + self.offset

    def adjust_time(self, adjustment):
        """
        Ajusta o horário do cliente.
        """
        with self.lock:
            before = self.offset
            self.offset += adjustment
            after = self.offset
            print(f"[+] Ajuste recebido: {adjustment:.2f} segundos (Antes: {before:.2f}, Depois: {after:.2f})")

    def run(self):
        """
        Simula o passar do tempo incrementando o relógio.
        """
        while self.running:
            time.sleep(1)  # Incrementa a cada segundo

def listen_to_server(sock, clock):
    """
    Escuta mensagens do servidor e age conforme o tipo da mensagem.
    """
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("[!] Conexão com o servidor perdida.")
                break
            message = json.loads(data.decode())
            if message["type"] == "TIME_REQUEST":
                current_time = clock.get_time()
                response = json.dumps({"type": "TIME", "time": current_time})
                sock.sendall(response.encode())
                print(f"[>] Enviando horário: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}")
            elif message["type"] == "ADJUST":
                adjustment = message["adjust"]
                before_adjust = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(clock.get_time()))
                clock.adjust_time(adjustment)
                after_adjust = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(clock.get_time()))
                print(f"[+] Horário antes do ajuste: {before_adjust}")
                print(f"[+] Horário após o ajuste:  {after_adjust}\n")
        except:
            print("[!] Erro na comunicação com o servidor.")
            break

def main():
    if len(sys.argv) > 1:
        try:
            initial_offset = float(sys.argv[1])
        except ValueError:
            print("Uso: python client.py [OFFSET]")
            sys.exit(1)
    else:
        initial_offset = OFFSET

    # Inicializa o relógio do cliente com um deslocamento
    clock = ClientClock(offset=initial_offset)

    # Conecta-se ao servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_HOST, SERVER_PORT))
        print(f"[+] Conectado ao servidor {SERVER_HOST}:{SERVER_PORT}")
    except Exception as e:
        print(f"[!] Não foi possível conectar ao servidor: {e}")
        sys.exit(1)

    # Inicia a thread para escutar mensagens do servidor
    listener_thread = threading.Thread(target=listen_to_server, args=(sock, clock), daemon=True)
    listener_thread.start()

    # Inicia a thread para simular o relógio do cliente
    clock_thread = threading.Thread(target=clock.run, daemon=True)
    clock_thread.start()

    try:
        while True:
            time.sleep(1)  # Mantém o programa rodando
    except KeyboardInterrupt:
        print("\n[!] Cliente encerrado.")
    finally:
        clock.running = False
        sock.close()

if __name__ == "__main__":
    main()
