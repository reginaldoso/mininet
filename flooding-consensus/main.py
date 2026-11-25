import argparse
import asyncio
import json

from consensus.consensus_node import ConsensusNode


async def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--value", type=int, required=True)
    parser.add_argument("--peers", type=str, required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--f", type=int, required=True)
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--timeout", type=float, default=5)

    args = parser.parse_args()

    if args.f < 0 or args.n <= args.f:
        raise ValueError("Configuração inválida de falhas")

    peers = json.loads(args.peers)

    peers = {
        int(process_id): ip
        for process_id, ip in peers.items()
    }

    node = ConsensusNode(
        process_id=args.id,
        initial_value=args.value,
        peers=peers,
        total_nodes=args.n,
        fault_limit=args.f,
        port=args.port,
        round_timeout=args.timeout
    )

    await node.run()


if __name__ == "__main__":
    asyncio.run(main())
