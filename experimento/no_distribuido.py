import socket
import sys

def rodar_no(porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', porta))
        s.listen(1)
        print(f"[ALGORITMO] Nó rodando e aguardando na porta {porta}...", flush=True)
        conn, addr = s.accept()
        with conn:
            print(f"[ALGORITMO] Conexão estabelecida com {addr}", flush=True)
            conn.sendall(b"OK: Algoritmo distribuido executado")

if __name__ == '__main__':
    porta_alvo = int(sys.argv[1]) if len(sys.argv) > 1 else 9000
    rodar_no(porta_alvo)