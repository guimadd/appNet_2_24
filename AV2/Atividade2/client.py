import socket
import threading
import json
import time
import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345        
OFFSET = 5                 

class ClientClock:
    def __init__(self, offset=0):
        self.lock = threading.Lock()
        self.offset = offset
        self.running = True

    def get_time(self):
        with self.lock:
            return time.time() + self.offset

    def adjust_time(self, adjustment):
        with self.lock:
            before = self.offset
            self.offset += adjustment
            after = self.offset
            print(f"[+] Ajuste recebido: {adjustment:.2f} segundos (Antes: {before:.2f}, Depois: {after:.2f})")

    def run(self):
        while self.running:
            time.sleep(1)  # Incrementa a cada segundo

def listen_to_server(sock, clock):
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
                readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                print(f"[>] Enviando horário: {readable_time}")
            elif message["type"] == "ADJUST":
                adjustment = message["adjust"]
                before_adjust = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(clock.get_time()))
                clock.adjust_time(adjustment)
                after_adjust = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(clock.get_time()))
                print(f"[+] Horário antes do ajuste: {before_adjust}")
                print(f"[+] Horário após o ajuste:  {after_adjust}\n")
        except json.JSONDecodeError:
            print("[!] Mensagem recebida inválida do servidor.")
        except Exception as e:
            print(f"[!] Erro na comunicação com o servidor: {e}")
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

    clock = ClientClock(offset=initial_offset)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_HOST, SERVER_PORT))
        print(f"[+] Conectado ao servidor {SERVER_HOST}:{SERVER_PORT}")
    except Exception as e:
        print(f"[!] Não foi possível conectar ao servidor: {e}")
        sys.exit(1)

    listener_thread = threading.Thread(target=listen_to_server, args=(sock, clock), daemon=True)
    listener_thread.start()

    clock_thread = threading.Thread(target=clock.run, daemon=True)
    clock_thread.start()

    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\n[!] Cliente encerrado.")
    finally:
        clock.running = False
        sock.close()

if __name__ == "__main__":
    main()
