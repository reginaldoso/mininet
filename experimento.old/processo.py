import socket
import threading
import time
import sys

# Importa a função do arquivo log.py
from log import log_formatado

def exec_servidor(porta_propria):
    end_servidor = ('0.0.0.0', porta_propria)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(end_servidor)
        s.listen(5)
        log_formatado("SERVIDOR", end_servidor, f"Nó escutando na porta {porta_propria}...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                dados = conn.recv(1024)
                log_formatado("SERVIDOR", addr, f"Mensagem recebida: {dados.decode('utf-8')}")
                conn.sendall(b"OK: Mensagem processada pelo no")

def exec_cliente(host_destino, porta_destino, mensagem):
    end_destino = (host_destino, porta_destino)
    log_formatado("CLIENTE", end_destino, "Conectando ao destino...")
    
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(end_destino)
                s.sendall(mensagem.encode('utf-8'))
                
                resposta = s.recv(1024)
                log_formatado("CLIENTE", end_destino, f"Resposta do destino: {resposta.decode('utf-8')}")
                break
        except ConnectionRefusedError:
            log_formatado("CLIENTE", end_destino, "Destino ainda não está pronto. Tentando novamente em 1 segundo...")
            time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python3 process.py <minha_porta> <ip_vizinho> <porta_vizinho>")
        sys.exit(1)

    MINHA_PORTA = int(sys.argv[1])
    HOST_VIZINHO = sys.argv[2]
    PORTA_VIZINHO = int(sys.argv[3])
    
    end_local = ('127.0.0.1', MINHA_PORTA)

    t_servidor = threading.Thread(target=exec_servidor, args=(MINHA_PORTA,), daemon=True)
    t_servidor.start()

    time.sleep(0.5)

    exec_cliente(HOST_VIZINHO, PORTA_VIZINHO, f"Olá vizinho, mensagem enviada da porta {MINHA_PORTA}!")

    log_formatado("NÓ", end_local, "Pressione CTRL+C para sair.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log_formatado("NÓ", end_local, "Encerrando...")