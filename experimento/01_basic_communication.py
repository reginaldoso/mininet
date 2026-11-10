# 01_basic_communication.py

import os
import time
from mininet.log import info
from config import HOST_1, HOST_2, CMD_H1, CMD_H2, LOG_DIR

def executar(net):
    # Cria a pasta 'logs' na raiz do projeto se ela não existir
    os.makedirs(LOG_DIR, exist_ok=True)

    info(f"\n*** Obtendo referências dos hosts no Mininet\n")
    h1 = net.get(HOST_1['name'])
    h2 = net.get(HOST_2['name'])

    info(f"*** Iniciando o processo no {HOST_2['name']} (Servidor/Cliente)...\n")
    h2.cmd(CMD_H2)
    
    # Pausa breve para garantir que o h2 abriu a porta do servidor
    time.sleep(1)

    info(f"*** Iniciando o processo no {HOST_1['name']} (Servidor/Cliente)...\n")
    h1.cmd(CMD_H1)

    info(f"\n*** Processos iniciados em background.\n")
    info(f"*** Salvando logs em: {LOG_DIR}/\n")
    info(f"*** Aguardando 5 segundos para a troca de mensagens...\n")
    time.sleep(5)

    info(f"\n*** Exibindo os logs coletados do Host 1 (h1):\n")
    info(h1.cmd(f"cat {LOG_DIR}/h1.log"))

    info(f"\n*** Exibindo os logs coletados do Host 2 (h2):\n")
    info(h2.cmd(f"cat {LOG_DIR}/h2.log"))

    info(f"\n*** Limpando processos python pendentes nos nós...\n")
    h1.cmd("pkill -f process.py")
    h2.cmd("pkill -f process.py")