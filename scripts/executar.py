# (Script orquestrador que monta a rede personalizada, inicia processos e executa os algoritmos)

#!/usr/bin/env python3
import os
import sys
import time

# Garante acesso ao diretório raiz para importar módulos de 'custom'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from mininet.net import Mininet
from mininet.node import Host
from mininet.node import OVSController
from mininet.log import setLogLevel, info
from custom.minha_topologia import TopologiaPersonalizada

def executar():
    # Pasta para salvar logs de execução dos algoritmos
    logs_dir = os.path.join(BASE_DIR, 'algoritmos', 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # 1. Carrega a topologia de custom/
    topo = TopologiaPersonalizada()
    net = Mininet(topo=topo, controller=OVSController)

    info("*** Criando e iniciando os objetos da rede...\n")
    net.start()

    try:
        h1 = net.get('h1')
        h2 = net.get('h2')

        info("*** Testando conectividade basica entre hosts...\n")
        net.ping([h1, h2])

        log_no = os.path.join(logs_dir, 'no_h2.log')
        log_cliente = os.path.join(logs_dir, 'cliente_h1.log')

        info("*** Executando algoritmo distribuido em h2...\n")
        # Inicia o algoritmo em segundo plano (&) em h2
        h2.cmd(f"python3 {BASE_DIR}/algoritmos/no_distribuido.py 9000 > {log_no} 2>&1 &")

        time.sleep(1)  # Aguarda a porta subir em h2

        info("*** Executando cliente auxiliar em h1...\n")
        # Executa o programa auxiliar em h1 de forma síncrona
        h1.cmd(f"python3 {BASE_DIR}/algoritmos/hosts/cliente_auxiliar.py {h2.IP()} 9000 > {log_cliente} 2>&1")

        info("*** Experimento finalizado! Logs salvos em algoritmos/logs/\n")

    finally:
        info("*** Parando a rede e limpando interfaces...\n")
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    executar()