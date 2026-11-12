import argparse
from functools import partial
import importlib
import json
import os
import sys
import traceback
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.topo import Topo
from mininet.clean import cleanup
from mininet.log import setLogLevel, info
from mininet.cli import CLI

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

PORTA_PADRAO = 5000

def gerar_mapa_rede(net):
    """ Mapeia os hosts e seus vizinhos reais (diretos ou via switch) """
    mapa = {}

    for h in net.hosts:
        vizinhos = []
        for intf in h.intfList():
            link = intf.link
            if not link:
                continue

            outra_ponta = link.intf1 if link.intf2 == intf else link.intf2
            outro_no = outra_ponta.node

            # Caso 1: Ligação direta host <-> host (anel sem switch)
            if outro_no.name.startswith('h') and outro_no.name != h.name:
                vizinhos.append(outra_ponta.IP())

            # Caso 2: Ligação via switch (host <-> switch <-> host)
            elif outro_no.name.startswith('s'):
                for sw_intf in outro_no.intfList():
                    sw_link = sw_intf.link
                    if sw_link:
                        viz_ponta = sw_link.intf1 if sw_link.intf2 == sw_intf else sw_link.intf2
                        viz_node = viz_ponta.node
                        if viz_node.name.startswith('h') and viz_node.name != h.name:
                            vizinhos.append(viz_ponta.IP())

        mapa[h.name] = {
            "ip": h.IP(),
            "vizinhos": list(set(vizinhos))
        }

    caminho_json = os.path.join(script_dir, "rede.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(mapa, f, indent=4)

    return mapa

def main():
    parser = argparse.ArgumentParser(description="Orquestrador de Experimentos Mininet")
    parser.add_argument('-t', '--topologia', type=str, required=True, help="Nome do arquivo de topologia (ex: topo_anel.py)")
    parser.add_argument('-n', '--nos', type=int, default=4, help="Quantidade de nós na topologia")
    args = parser.parse_args()

    setLogLevel('error')
    cleanup()
    setLogLevel('info')

    processos = []
    net = None

    try:
        # Extrai apenas o nome do módulo mesmo se o usuário passar 'topologias/topo_anel.py'
        arquivo_topo = os.path.basename(args.topologia)
        nome_topo = arquivo_topo[:-3] if arquivo_topo.endswith('.py') else arquivo_topo

        mod_topo = importlib.import_module(f"topologias.{nome_topo}")
        ClasseTopo = next(
            obj for obj in vars(mod_topo).values()
            if isinstance(obj, type) and issubclass(obj, Topo) and obj is not Topo
        )

        switch_standalone = partial(OVSSwitch, failMode='standalone')
        net = Mininet(topo=ClasseTopo(num_hosts=args.nos), switch=switch_standalone, controller=None)
        net.start()

        dir_logs = os.path.join(script_dir, "logs")
        os.makedirs(dir_logs, exist_ok=True)

        mapa = gerar_mapa_rede(net)

        info(f"\n*** Rede iniciada! Subindo nós na porta {PORTA_PADRAO}...\n")
        caminho_nodo = os.path.join(script_dir, "nodo.py")

        for host in net.hosts:
            log_path = os.path.join(dir_logs, f"{host.name}.log")
            log_file = open(log_path, "w", encoding="utf-8")

            proc = host.popen(["python3", "-u", caminho_nodo, host.name], stdout=log_file, stderr=log_file)
            processos.append((proc, log_file))
            info(f"  -> Nó {host.name} ({mapa[host.name]['ip']}:{PORTA_PADRAO}) ativo.\n")

        info("\n*** Experimento em execução. Digite 'exit' no CLI do Mininet para encerrar.\n")
        CLI(net)

    except Exception as e:
        info(f"\n[ERRO]: {e}\n")
        traceback.print_exc()

    finally:
        info("\n*** Encerrando processos dos nós e limpando conexões...\n")
        for proc, log_f in processos:
            try:
                proc.terminate()
            except Exception:
                pass
            log_f.close()

        if net is not None:
            setLogLevel('error')
            net.stop()
        setLogLevel('info')
        info("*** Experimento finalizado!\n")

if __name__ == '__main__':
    setLogLevel('info')
    main()