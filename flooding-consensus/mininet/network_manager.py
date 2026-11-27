import os
import sys
import json
import time
import argparse
from pathlib import Path
from mininet.net import Mininet
from mininet.node import Controller
from mininet.topo import SingleSwitchTopo
from mininet.cli import CLI
from mininet.log import setLogLevel

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.failure_injector import FailureInjector

def start_experiment(n=5, f=1):

    if n <= f or f < 0:
        raise ValueError("Parâmetros inválidos")

    os.chdir(PROJECT_ROOT)

    os.makedirs("results/logs", exist_ok=True)
    os.makedirs("results/metrics", exist_ok=True)

    topo = SingleSwitchTopo(k=n)

    net = Mininet(
        topo=topo,
        controller=Controller,
        autoSetMacs=True
    )

    processes = []

    try:

        net.start()

        hosts = net.hosts

        peers = {
            i: f"10.0.0.{i}"
            for i in range(1, n + 1)
        }

        peers_json = json.dumps(peers)

        print("\n===== INICIANDO CONSENSO =====\n")

        time.sleep(2)

        for i, host in enumerate(hosts, start=1):

            value = i * 10

            command = [
                "python3",
                str(PROJECT_ROOT / "main.py"),
                "--id", str(i),
                "--value", str(value),
                "--peers", peers_json,
                "--n", str(n),
                "--f", str(f),
                "--port", "5000",
                "--timeout", "5"
            ]

            logfile = open(
                f"results/logs/process_{i}.log",
                "w"
            )

            process = host.popen(
                command,
                cwd=str(PROJECT_ROOT),
                stdout=logfile,
                stderr=logfile
            )

            processes.append((process, logfile))

        print("\nProcessos iniciados.")

        print("Topologia:", net.topo)

        CLI(net)

    finally:

        print("\nEncerrando processos...")

        for process, logfile in processes:

            if process.poll() is None:
                process.terminate()

            logfile.close()

        net.stop()


if __name__ == "__main__":

    setLogLevel("info")

    parser = argparse.ArgumentParser()

    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--f", type=int, default=1)

    parser.add_argument(
    "--failure",
    choices=["none", "random", "manual"],
    default="none"
    )

    parser.add_argument(
        "--fail-count",
        type=int,
        default=0
    )

    parser.add_argument(
        "--fail-nodes",
        type=str,
        default=""
    )

    parser.add_argument(
        "--fail-round",
        type=int,
        default=1
    )


    args = parser.parse_args()

    start_experiment(
        n=args.n,
        f=args.f
    )
    failure_injector = FailureInjector(
    mode=args.failure,
    fail_nodes=[
        int(x) for x in args.fail_nodes.split(",") if x
    ],
    fail_count=args.fail_count,
    fail_round=args.fail_round
    )

    nodes_to_fail = failure_injector.select_nodes(args.n)
