# Orquestrador da rede e gerador do rede.json



import argparse
import importlib
import json
import os
import sys
import subprocess
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

PORTA_PADRAO = 5000

def gerar_mapa_rede(net):
    """ Mapeia os hosts e seus vizinhos reais, salvando em rede.json """
    mapa = {}
    hosts = net.hosts

    for h in hosts:
        vizinhos = []
        for intf in h.intfList():
            link = intf.link
            if not link:
                continue
            outro_no = link.intf1.node if link.intf2.node == h else link.intf2.node
            
            if outro_no.name.startswith('s'):
                for sw_intf in outro_no.intfList():
                    sw_link = sw_intf.link
                    if sw_link:
                        viz_node = sw_link.intf1.node if sw_link.intf2.node == outro_no else sw_link.intf2.node
                        if viz_node.name.startswith('h') and viz_node.name != h.name:
                            vizinhos.append(viz_node.IP())

        mapa[h.name] = {
            "ip": h.IP(),
            "vizinhos": list(set(vizinhos))
        }

    caminho_json = os.path.join(script_dir, "rede.json")
    with open(caminho_json, "w") as f:
        json.dump(mapa, f, indent=4)
    
    return mapa

def main():
    parser = argparse.ArgumentParser(description="Orquestrador de Experimentos Mininet")
    parser.add_argument('-t', '--topologia', type=str, required=True, help="Nome do arquivo de topologia (ex: topo_anel.py)")
    parser.add_argument('-n', '--nos', type=int, default=4, help="Quantidade de nós na topologia")
    args = parser.parse_args()

    info("\n*** Limpando recursos residuais do Mininet...\n")
    subprocess.run(['mn', '-c'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    nome_topo = args.topologia[:-3] if args.topologia.endswith('.py') else args.topologia
    mod_topo = importlib.import_module(f"topologias.{nome_topo}")
    ClasseTopo = next(obj for attr, obj in vars(mod_topo).items() if isinstance(obj, type) and attr.startswith('Topo'))

    net = Mininet(topo=ClasseTopo(num_hosts=args.nos), switch=OVSSwitch)
    processos = []

    try:
        net.start()

        dir_logs = os.path.join(script_dir, "logs")
        os.makedirs(dir_logs, exist_ok=True)
        
        mapa = gerar_mapa_rede(net)

        info(f"\n*** Rede iniciada! Subindo nós com a porta {PORTA_PADRAO}...\n")
        caminho_nodo = os.path.join(script_dir, "nodo.py")

        for host in net.hosts:
            log_path = os.path.join(dir_logs, f"{host.name}.log")
            log_file = open(log_path, "w")

            # Executa o nodo.py passando apenas o nome do host
            proc = host.popen(["python3", "-u", caminho_nodo, host.name], stdout=log_file, stderr=log_file)
            processos.append((proc, log_file))
            info(f"  -> Nó {host.name} ({mapa[host.name]['ip']}:{PORTA_PADRAO}) ativo.\n")

        info("\n*** Experimento em execução. Digite 'exit' no CLI do Mininet para encerrar.\n")
        CLI(net)

    except Exception as e:
        info(f"\n[ERRO]: {e}\n")

    finally:
        info("\n*** Encerrando processos dos nós e limpando conexões...\n")
        for proc, log_f in processos:
            try:
                proc.terminate()
            except Exception:
                pass
            log_f.close()

        if 'net' in locals():
            net.stop()
        info("*** Experimento finalizado!\n")

if __name__ == '__main__':
    setLogLevel('info')
    main()