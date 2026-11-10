import socket
import threading
import time
import sys

def exec_servidor(porta_propria):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', porta_propria))
        s.listen(5)
        print(f"[SERVIDOR] Nó escutando na porta {porta_propria}...", flush=True)
        
        while True:
            conn, addr = s.accept()
            with conn:
                dados = conn.recv(1024)
                print(f"[SERVIDOR] Mensagem recebida de {addr}: {dados.decode('utf-8')}", flush=True)
                conn.sendall(b"OK: Mensagem processada pelo no")

def exec_cliente(host_destino, porta_destino, mensagem):
    print(f"[CLIENTE] Conectando ao destino {host_destino}:{porta_destino}...", flush=True)
    
    # Loop de tentativas de conexões
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host_destino, porta_destino))
                s.sendall(mensagem.encode('utf-8'))
                
                resposta = s.recv(1024)
                print(f"[CLIENTE] Resposta do destino: {resposta.decode('utf-8')}", flush=True)
                break  # Conexão bem-sucedida, sai do loop
        except ConnectionRefusedError:
            print(f"[CLIENTE] Destino ainda não está pronto. Tentando novamente em 1 segundo...", flush=True)
            time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python3 process.py <minha_porta> <ip_vizinho> <porta_vizinho>")
        sys.exit(1)

    MINHA_PORTA = int(sys.argv[1])
    HOST_VIZINHO = sys.argv[2]
    PORTA_VIZINHO = int(sys.argv[3])

    # Inicia a thread do servidor em segundo plano
    t_servidor = threading.Thread(target=exec_servidor, args=(MINHA_PORTA,), daemon=True)
    t_servidor.start()

    # Pequena pausa para garantir que o socket local abriu
    time.sleep(0.5)

    # Inicia o cliente tentando falar com o vizinho
    exec_cliente(HOST_VIZINHO, PORTA_VIZINHO, f"Olá vizinho, mensagem enviada da porta {MINHA_PORTA}!")

    # Mantém o script rodando para o servidor continuar escutando
    print("[NÓ] Pressione CTRL+C para sair.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[NÓ] Encerrando...")