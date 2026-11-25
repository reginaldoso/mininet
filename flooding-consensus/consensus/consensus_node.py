import asyncio
from collections import defaultdict

from events.event_manager import EventManager
from events.message_handler import MessageHandler
from communication.socket_manager import SocketManager
from consensus.flooding_algorithm import FloodingAlgorithm
from consensus.round_manager import RoundManager
from experiments.metrics_collector import MetricsCollector


class ConsensusNode:

    def __init__(
        self,
        process_id,
        initial_value,
        peers,
        total_nodes,
        fault_limit,
        port=5000,
        round_timeout=5
    ):

        self.process_id = process_id
        self.values = {initial_value}
        self.peers = peers

        self.total_nodes = total_nodes
        self.fault_limit = fault_limit
        self.round_timeout = round_timeout

        self.round_manager = RoundManager(fault_limit)

        self.round_number = 1

        self.received_messages = defaultdict(set)

        self.event_manager = EventManager()

        self.message_handler = MessageHandler(self)

        self.socket_manager = SocketManager(
            self,
            port
        )

        self.algorithm = FloodingAlgorithm(self)

        self.metrics = MetricsCollector(
            process_id
        )

    async def run(self):

        print(
            f"[P{self.process_id}] "
            f"Iniciando com valor {self.values}"
        )

        await self.socket_manager.start()

        # Tempo para inicialização dos sockets.
        await asyncio.sleep(1)

        success = True

        try:

            while self.round_manager.has_next_round():

                self.round_number = (
                    self.round_manager.get_current_round()
                )

                completed = await self.algorithm.execute_round()

                if not completed:
                    success = False
                    break

                self.round_manager.advance()

            decision = None

            if success:
                decision = self.algorithm.calculate_decision()

                await self.event_manager.publish(
                    "CONSENSUS_REACHED",
                    decision
                )

                print(
                    f"[P{self.process_id}] "
                    f"Decisão final: {decision}"
                )

            self.metrics.save(
                decision,
                self.round_number if success else (
                    self.round_number - 1
                ),
                success
            )

        finally:
            self.socket_manager.close()

        return decision
