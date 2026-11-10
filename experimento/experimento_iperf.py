# experimento_iperf.py
from config import HOST_1, HOST_2

def executar(net):
    """Função padrão de execução para o iperf."""
    h1 = net.get(HOST_1['name'])
    h2 = net.get(HOST_2['name'])

    print(f'\n*** Iniciando servidor iperf em {HOST_2["name"]}')
    h2.cmd('iperf -s &')

    print(f'\n*** Executando cliente iperf de {HOST_1["name"]} para {HOST_2["name"]}')
    resultado = h1.cmd(f'iperf -c {HOST_2["ip"].split("/")[0]} -t 5')
    print(resultado)

    h2.cmd('killall iperf')