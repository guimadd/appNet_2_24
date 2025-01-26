import socket
import struct
import time
import datetime

def ntp_client(host="pool.ntp.org", port=123):
    servidor = (host, port)
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente.settimeout(5) 

    pacote = b'\x1b' + 47 * b'\0'
    
    try: 
        tempoEnviado = time.time()
        cliente.sendto(pacote, servidor)

        dados, _ = cliente.recvfrom(1024)
        tempoRecebido = time.time()

        atraso = tempoRecebido - tempoEnviado
        
        unpacked = struct.unpack('!12I', dados[0:48])
        ntp_timestamp = unpacked[10]
        
        UNIX_EPOCH_DIFF = 2208988800
        tempo_unix = ntp_timestamp - UNIX_EPOCH_DIFF
        
        dt = datetime.datetime.fromtimestamp(tempo_unix)
        
        dias_pt = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

        meses_pt = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                    "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        
        dia_semana = dias_pt[dt.weekday()]
        dia = dt.day
        mes = meses_pt[dt.month - 1]
        ano = dt.year
        hora_formatada = dt.strftime("%H:%M:%S")
        
        data_hora_formatada = f"{hora_formatada}, {dia_semana} {dia} {mes} {ano}"
        
        print("Data/Hora (servidor NTP) :", data_hora_formatada)
        print(f"Atraso (round-trip)     : {atraso:.6f} segundos")
        
    except socket.timeout:
        print("O servidor NTP não respondeu dentro do tempo limite.")
    finally:
        cliente.close()

if __name__ == "__main__":
    ntp_client()