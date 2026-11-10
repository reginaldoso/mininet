# Parâmetros de Rede e Configuração
# Este arquivo armazena todas as constantes, IPs e caminhos de
# arquivos usados no experimento.

import os

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


# Caminho absoluto para a pasta do projeto e criação da pasta logs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
PROCESS_PATH = os.path.join(BASE_DIR, 'processo.py') # Caminho absoluto do script

# Parâmetros de portas para o script process.py
PORTA_H1 = 5001
PORTA_H2 = 5002

# Comandos utilizando o caminho absoluto do process.py e da pasta logs
CMD_H1 = f"python3 {PROCESS_PATH} {PORTA_H1} {HOST_2['ip'].split('/')[0]} {PORTA_H2} > {LOG_DIR}/h1.log 2>&1 &"
CMD_H2 = f"python3 {PROCESS_PATH} {PORTA_H2} {HOST_1['ip'].split('/')[0]} {PORTA_H1} > {LOG_DIR}/h2.log 2>&1 &"