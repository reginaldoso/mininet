import socket
import sys

def conectar(ip_destino, porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip_destino, porta))
        resposta = s.recv(1024)
        print(f"[HOST AUXILIAR] Resposta do algoritmo: {resposta.decode()}", flush=True)

if __name__ == '__main__':
    ip = sys.argv[1]
    porta = int(sys.argv[2])
    conectar(ip, porta)