import asyncio
import socket


class UDPReceiver(asyncio.DatagramProtocol):

    def __init__(self, node):
        self.node = node

    def datagram_received(self, data, addr):
        asyncio.create_task(
            self.node.message_handler.handle(data)
        )


class SocketManager:

    def __init__(self, node, port=5000):
        self.node = node
        self.port = port
        self.transport = None

    async def start(self):

        loop = asyncio.get_running_loop()

        self.transport, _ = await loop.create_datagram_endpoint(
            lambda: UDPReceiver(self.node),
            local_addr=("0.0.0.0", self.port)
        )

    async def send(self, data, destination):

        if self.transport is None:
            raise RuntimeError("Socket não inicializado")

        self.transport.sendto(
            data,
            (destination, self.port)
        )
        self.node.metrics.register_sent()

    def close(self):

        if self.transport:
            self.transport.close()
