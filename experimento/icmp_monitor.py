# experimento/icmp_monitor.py

import time
from config import (
    HOST_1,
    HOST_2,
    CAPTURE_FILE,
    PID_FILE,
    PING_COUNT,
    TCPDUMP_CMD,
)


def executar(net):
    """Função principal executada pelo main.py para monitorar pacotes ICMP."""
    h1 = net.get(HOST_1['name'])
    h2 = net.get(HOST_2['name'])

    print(f'\n*** Iniciando captura ICMP em {HOST_1["name"]}')
    h1.cmd(f'rm -f {CAPTURE_FILE}')

    # Monta e executa o comando do tcpdump em background
    comando_tcpdump = TCPDUMP_CMD.format(
        interface=HOST_1['interface'],
        capture_file=CAPTURE_FILE,
        pid_file=PID_FILE,
    )
    h1.cmd(comando_tcpdump)

    # Aguarda o PID do tcpdump ser gerado
    pid = None
    for _ in range(30):
        pid = h1.cmd(f'cat {PID_FILE} 2>/dev/null').strip()
        if pid:
            break
        time.sleep(0.1)

    if not pid:
        raise RuntimeError('Não foi possível iniciar o tcpdump.')

    print(f'*** PID do tcpdump: {pid}')

    try:
        # Executa o ping
        print(f'\n*** Executando ping de {HOST_1["name"]} para {HOST_2["name"]}')
        resultado = h1.cmd(f'ping -c {PING_COUNT} {HOST_1["ping_target"]}')
        print(resultado)

    finally:
        # O bloco finally garante que a captura será encerrada e exibida,
        # aconteça o que acontecer durante o ping.
        _finalizar_captura(h1, pid)


def _finalizar_captura(h1, pid):
    """Encerra o tcpdump de forma segura e exibe os pacotes capturados."""
    print('\n*** Encerrando captura')
    h1.cmd(f'kill -INT {pid}')

    # Aguarda o processo encerrar
    encerrado = False
    for _ in range(50):
        estado = h1.cmd(f'ps -p {pid} -o stat= 2>/dev/null').strip()
        if not estado or estado.startswith('Z'):
            encerrado = True
            break
        time.sleep(0.1)

    if not encerrado:
        print('*** Tempo limite atingido. Enviando SIGKILL.')
        h1.cmd(f'kill -KILL {pid}')
        time.sleep(0.2)

    # Exibe os pacotes salvos no arquivo temporário
    print('\n*** Pacotes capturados:')
    saida = h1.cmd(f'cat {CAPTURE_FILE}')
    print(saida)

    # Limpa os arquivos temporários
    h1.cmd(f'rm -f {CAPTURE_FILE} {PID_FILE}')