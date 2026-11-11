# main.py
from mininet.cli import CLI
import argparse
import importlib
import os
import sys
import subprocess
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.log import setLogLevel, info

# 1. Descobre a pasta onde este script (main.py) está e a adiciona ao path do Python
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from topologia import MinhaTopo


def main():
    parser = argparse.ArgumentParser(
        description='Executa simulações no Mininet carregando dinamicamente um arquivo de experimento.'
    )
    parser.add_argument(
        '-e', '--experimento',
        type=str,
        required=True,
        help='Nome do arquivo do experimento (ex: icmp_monitor)'
    )
    args = parser.parse_args()

    # Remove a extensão '.py' caso o usuário digite
    nome_modulo = args.experimento
    if nome_modulo.endswith('.py'):
        nome_modulo = nome_modulo[:-3]

    # 2. Verifica se o arquivo existe na mesma pasta do main.py
    caminho_arquivo = os.path.join(script_dir, f'{nome_modulo}.py')
    if not os.path.exists(caminho_arquivo):
        info(f'\n[ERRO] O arquivo "{nome_modulo}.py" não foi encontrado em: {script_dir}\n')
        return

    info(f'\n*** Limpando recursos do Mininet\n')
    subprocess.run(['mn', '-c'], check=True)

    topo = MinhaTopo()
    net = Mininet(topo=topo, switch=OVSSwitch)

    try:
        net.start()
        info(f'\n*** Rede iniciada! Carregando experimento: [{nome_modulo}.py]\n')

        # Importa o módulo dinamicamente
        modulo_experimento = importlib.import_module(nome_modulo)

        # Verifica se o módulo possui a função padrão 'executar'
        if not hasattr(modulo_experimento, 'executar'):
            info(f'\n[ERRO] O arquivo "{nome_modulo}.py" não possui a função obrigatória "executar(net)"!\n')
            return

        # Executa a lógica
        modulo_experimento.executar(net)
        info('\n*** Experimento concluído. Abrindo a CLI do Mininet (digite "exit" para sair)...\n')
        CLI(net)

    except Exception as e:
        info(f'\n*** Ocorreu um erro durante o experimento: {e}\n')

    finally:
        info('\n*** Encerrando Mininet\n')
        net.stop()
        info('\n*** Experimento finalizado!\n')


if __name__ == '__main__':
    setLogLevel('info')
    main()