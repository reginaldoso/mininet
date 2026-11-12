import sys
import os
import json
import socket
import threading
import time
from log import log_formatado

if len(sys.argv) < 2:
    print("Uso: python3 nodo.py <nome_do_host>")
    sys.exit(1)

NOME_HOST = sys.argv[1]
PORTA_PADRAO = 5000

script_dir = os.path.dirname(os.path.abspath(__file__))
caminho_json = os.path.join(script_dir, "rede.json")

with open(caminho_json, "r", encoding="utf-8") as f:
    MAPA_REDE = json.load(f)

MEU_CONFIG = MAPA_REDE[NOME_HOST]
MEU_IP = MEU_CONFIG["ip"]
VIZINHOS_IPS = MEU_CONFIG["vizinhos"]

mensagens_vistas = set()

def escutar_servidor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # '0.0.0.0' permite receber pacotes em qualquer interface do host (eth0, eth1, etc.)
    sock.bind(("0.0.0.0", PORTA_PADRAO))
    log_formatado("SERVIDOR", (MEU_IP, PORTA_PADRAO), f"Nó {NOME_HOST} online. Vizinhos: {VIZINHOS_IPS}")

    while True:
        dados, addr_remoto = sock.recvfrom(1024)
        msg = dados.decode('utf-8')

        if msg not in mensagens_vistas:
            mensagens_vistas.add(msg)
            log_formatado("INUNDACAO", addr_remoto, f"Recebeu: {msg}")

            for ip_vizinho in VIZINHOS_IPS:
                if ip_vizinho != addr_remoto[0]:
                    sock.sendto(msg.encode('utf-8'), (ip_vizinho, PORTA_PADRAO))

if __name__ == "__main__":
    t = threading.Thread(target=escutar_servidor, daemon=True)
    t.start()

    if NOME_HOST == "h1":
        time.sleep(2)
        sock_envio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg_inicial = "MSG_TESTE_01"
        mensagens_vistas.add(msg_inicial)
        log_formatado("INICIADOR", (MEU_IP, PORTA_PADRAO), "Iniciando inundação na rede...")

        for ip_vizinho in VIZINHOS_IPS:
            sock_envio.sendto(msg_inicial.encode('utf-8'), (ip_vizinho, PORTA_PADRAO))

    while True:
        time.sleep(1)