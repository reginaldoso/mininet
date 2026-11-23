import os
import sys
import time
from mininet.net import Mininet
from mininet.topo import SingleSwitchTopo
from mininet.node import OVSKernelSwitch, DefaultController
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def iniciar_ambiente():
    # ETAPA 1: Criar e iniciar a topologia (1 switch L2 + 3 hosts)
    info("*** [Etapa 1] Iniciando topologia no Mininet...\n")
    topo = SingleSwitchTopo(k=3)
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        controller=DefaultController,
        autoSetMacs=True
    )
    net.start()

    h1, h2, h3 = net.get('h1', 'h2', 'h3')

    # ETAPA 2: Criar o script emissor broadcast.py usando apenas Python nativo (socket)
    info("*** [Etapa 2] Criando script 'broadcast.py' para o h1...\n")
    codigo_emissor = """import socket
import struct

def checksum(dados):
    if len(dados) % 2:
        dados += b'\\x00'
    s = sum(struct.unpack('!%dH' % (len(dados) // 2), dados))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return ~s & 0xffff

payload = b"OLA REDE! Datagrama personalizado em broadcast."

# Cabeçalho UDP (sport=12345, dport=9999)
udp_len = 8 + len(payload)
udp_hdr = struct.pack('!HHHH', 12345, 9999, udp_len, 0)

# Cabeçalho IPv4 (10.0.0.1 -> 255.255.255.255, proto UDP=17)
ip_tot_len = 20 + udp_len
ip_hdr_sem_csum = struct.pack('!BBHHHBBH4s4s',
    0x45, 0, ip_tot_len, 54321, 0, 64, 17, 0,
    socket.inet_aton('10.0.0.1'),
    socket.inet_aton('255.255.255.255')
)
ip_hdr = struct.pack('!BBHHHBBH4s4s',
    0x45, 0, ip_tot_len, 54321, 0, 64, 17, checksum(ip_hdr_sem_csum),
    socket.inet_aton('10.0.0.1'),
    socket.inet_aton('255.255.255.255')
)

# Cabeçalho Ethernet (dst=ff:ff:ff:ff:ff:ff, src=00:00:00:00:00:01, type=IPv4 0x0800)
eth_hdr = b'\\xff\\xff\\xff\\xff\\xff\\xff' + b'\\x00\\x00\\x00\\x00\\x00\\x01' + b'\\x08\\x00'

pacote = eth_hdr + ip_hdr + udp_hdr + payload

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
s.bind(("h1-eth0", 0))
s.send(pacote)
s.close()
print("Quadro broadcast enviado com sucesso!")
"""
    with open("broadcast.py", "w") as f:
        f.write(codigo_emissor)

    # ETAPA 3: Abrir janelas xterm individuais para h2 e h3 já escutando a rede
    info("*** [Etapa 3] Abrindo terminais individuais (xterm) para h2 e h3...\n")
    h2.cmd('xterm -title "Host h2 - Escutando" -e "tcpdump -l -i h2-eth0 -nn -e -A udp port 9999" &')
    h3.cmd('xterm -title "Host h3 - Escutando" -e "tcpdump -l -i h3-eth0 -nn -e -A udp port 9999" &')

    time.sleep(1)

    # Abre a CLI do Mininet para você executar a Etapa 4
    info("\n*** Ambiente pronto! Execute na CLI: h1 python3 broadcast.py\n")
    CLI(net)

    # Limpeza ao sair da CLI (exit)
    info("*** Encerrando processos e limpando ambiente...\n")
    h2.cmd("killall -9 tcpdump")
    if os.path.exists("broadcast.py"):
        os.remove("broadcast.py")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    iniciar_ambiente()
