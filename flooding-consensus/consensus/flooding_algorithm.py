import asyncio

from communication.message import Message
from events.timer_handler import TimerHandler


class FloodingAlgorithm:

    def __init__(self, node):
        self.node = node

    async def broadcast_values(self):

        message = Message(
            sender=self.node.process_id,
            round_number=self.node.round_number,
            values=sorted(self.node.values)
        )

        for peer_id, peer_ip in self.node.peers.items():

            if peer_id == self.node.process_id:
                continue

            await self.node.socket_manager.send(
                message.serialize(),
                peer_ip
            )

        await self.node.event_manager.publish(
            "MESSAGE_SENT",
            {
                "round": self.node.round_number,
                "values": sorted(self.node.values)
            }
        )

    async def wait_for_messages(self):

        required_messages = (
            self.node.total_nodes
            - self.node.fault_limit
            - 1
        )

        if required_messages <= 0:
            return True

        deadline = (
            asyncio.get_running_loop().time()
            + self.node.round_timeout
        )

        while True:

            received = self.node.received_messages[
                self.node.round_number
            ]

            if len(received) >= required_messages:
                return True

            remaining = (
                deadline - asyncio.get_running_loop().time()
            )

            if remaining <= 0:
                return False

            await TimerHandler.wait(
                min(0.05, remaining)
            )

    async def execute_round(self):

        await self.node.event_manager.publish(
            "ROUND_STARTED",
            self.node.round_number
        )

        await self.broadcast_values()

        completed = await self.wait_for_messages()

        if not completed:

            print(
                f"[P{self.node.process_id}] "
                f"Timeout na rodada {self.node.round_number}"
            )

            return False

        await self.node.event_manager.publish(
            "ROUND_COMPLETED",
            self.node.round_number
        )

        return True

    def calculate_decision(self):

        if not self.node.values:
            raise RuntimeError("Conjunto de valores vazio")

        return min(self.node.values)
