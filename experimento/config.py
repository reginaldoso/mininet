# Parâmetros de Rede e Configuração
# Este arquivo armazena todas as constantes, IPs e caminhos de
# arquivos usados no experimento.

# config.py

# Parâmetros dos Hosts
HOST_1 = {
    'name': 'h1',
    'ip': '10.0.0.1/24',
    'ping_target': '10.0.0.2',
    'interface': 'h1-eth0',
}

HOST_2 = {
    'name': 'h2',
    'ip': '10.0.0.2/24',
}

# Parâmetros do Switch
SWITCH_NAME = 's1'

# Configurações de Captura e Arquivos Temporários
CAPTURE_FILE = '/tmp/captura_icmp.txt'
PID_FILE = '/tmp/tcpdump.pid'
PING_COUNT = 4

# Comando tcpdump formatado para injetar interface dinamicamente
TCPDUMP_CMD = (
    'tcpdump -l -i {interface} -n -tttt icmp '
    '> {capture_file} 2>&1 & echo $! '
    '> {pid_file}'
)