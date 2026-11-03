#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.util import custom
from mininet.log import setLogLevel
from mininet.clean import cleanup
from mininet.cli import CLI
import argparse
import yaml
import sys
import os

class FullMeshNoSwitchTopo(Topo):
    "Topologia Full Mesh N:N sem switches com distribuição de CPU."

    def build(self, num_hosts=4, cpu_limit=0.10, core_a='1', core_b='2'):
        if num_hosts < 2:
            print("Erro: A topologia N para N requer no mínimo 2 hosts.")
            sys.exit(1)

        hosts = []

        # 1. Criar os hosts e distribuir entre os dois núcleos de CPU
        for i in range(1, num_hosts + 1):
            assigned_core = core_a if (i % 2 != 0) else core_b

            host_cls = custom(
                CPULimitedHost,
                cpu=cpu_limit,
                cores=assigned_core,
                sched='cfs'
            )

            h = self.addHost(
                f'h{i}',
                cls=host_cls,
                ip=f'10.0.0.{i}/8'
            )
            hosts.append(h)

        # 2. Conectar todos os hosts entre si em Full Mesh (N*(N-1)/2 links)
        for i in range(len(hosts)):
            for j in range(i + 1, len(hosts)):
                self.addLink(hosts[i], hosts[j])


def load_yaml_config(config_path="config.yaml"):
    """Carrega as configurações do YAML se o arquivo existir."""
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Aviso: Erro ao ler '{config_path}': {e}. Usando valores padrão.")
    return None


def parse_args():
    """Lê os argumentos opcionais da linha de comando."""
    parser = argparse.ArgumentParser(
        description="Topologia Customizada Mininet: Full Mesh N:N sem switches."
    )
    parser.add_argument('--config', type=str, default='config.yaml', help="Caminho do arquivo YAML")
    parser.add_argument('-n', '--hosts', type=int, default=None, help="Quantidade de hosts N (sobrescreve o YAML)")
    parser.add_argument('-c', '--cpu', type=float, default=None, help="Limite de CPU por host (sobrescreve o YAML)")
    parser.add_argument('--coreA', type=str, default=None, help="Primeiro núcleo isolado (sobrescreve o YAML)")
    parser.add_argument('--coreB', type=str, default=None, help="Segundo núcleo isolado (sobrescreve o YAML)")
    return parser.parse_args()


# Permite carregar a topologia via comando 'mn --custom'
topos = {
    'fullmesh_noswitch': (lambda **kwargs: FullMeshNoSwitchTopo(**kwargs))
}


def runExperiment():
    cleanup()
    args = parse_args()
    
    # 1. Carrega as configurações do arquivo YAML
    yaml_cfg = load_yaml_config(args.config)

    # Valores padrão de fallback caso nem o YAML nem a CLI forneçam dados
    default_hosts = 4
    default_cpu = 0.10
    default_core_a = '1'
    default_core_b = '2'

    # 2. Define os valores finais respeitando a prioridade: CLI > YAML > Padrão
    if yaml_cfg:
        num_hosts = args.hosts if args.hosts is not None else yaml_cfg.get('topology', {}).get('num_hosts', default_hosts)
        cpu_limit = args.cpu if args.cpu is not None else yaml_cfg.get('topology', {}).get('cpu_limit', default_cpu)
        core_a = str(args.coreA if args.coreA is not None else yaml_cfg.get('cpu_isolation', {}).get('core_a', default_core_a))
        core_b = str(args.coreB if args.coreB is not None else yaml_cfg.get('cpu_isolation', {}).get('core_b', default_core_b))
    else:
        num_hosts = args.hosts if args.hosts is not None else default_hosts
        cpu_limit = args.cpu if args.cpu is not None else default_cpu
        core_a = str(args.coreA if args.coreA is not None else default_core_a)
        core_b = str(args.coreB if args.coreB is not None else default_core_b)

    print(f"\n*** Inicializando Experimento N:N (Full Mesh)")
    print(f"*** Origem dos Parâmetros: {'CLI / YAML' if yaml_cfg else 'Padrão / CLI'}")
    print(f"*** Hosts: {num_hosts} | CPU/host: {cpu_limit*100:.1f}% | Cores: {core_a} e {core_b}")

    # 3. Instancia a topologia customizada
    topo = FullMeshNoSwitchTopo(
        num_hosts=num_hosts,
        cpu_limit=cpu_limit,
        core_a=core_a,
        core_b=core_b
    )

    # 4. Instancia e inicia o Mininet
    net = Mininet(topo=topo, build=False)
    net.build()
    net.start()

    # 5. Configuração dinâmica das sub-redes /30 nos links diretos
    print("\n*** Configurando IPs secundários (/30) nos links diretos...")
    hosts = [net.get(f'h{i}') for i in range(1, num_hosts + 1)]
    subnet_counter = 1

    for i in range(len(hosts)):
        for j in range(i + 1, len(hosts)):
            h_src, h_dst = hosts[i], hosts[j]

            intf_src = h_src.connectionsTo(h_dst)[0][0]
            intf_dst = h_src.connectionsTo(h_dst)[0][1]

            intf_src.setIP(f"192.168.{subnet_counter}.1/30")
            intf_dst.setIP(f"192.168.{subnet_counter}.2/30")

            subnet_counter += 1

    # Resumo do alocamento de CPU
    print("\n--- DISTRIBUIÇÃO DOS HOSTS NOS NÚCLEOS DE CPU ---")
    for h in hosts:
        print(f"Host {h.name} -> Core: {h.params.get('cores')} | Limite: {h.params.get('cpu')*100:.1f}%")
    print("--------------------------------------------------\n")

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    runExperiment()