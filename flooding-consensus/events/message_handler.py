from communication.message import Message


class MessageHandler:

    def __init__(self, node):
        self.node = node

    async def handle(self, data):

        try:
            message = Message.deserialize(data)

            self.node.metrics.register_received()

            if message.sender == self.node.process_id:
                return

            if message.round_number > self.node.round_number:
                return

            self.node.received_messages[
                message.round_number
            ].add(message.sender)

            self.node.values.update(message.values)

            await self.node.event_manager.publish(
                "MESSAGE_RECEIVED",
                {
                    "sender": message.sender,
                    "round": message.round_number,
                    "values": message.values
                }
            )

        except Exception as error:
            print(
                f"[P{self.node.process_id}] "
                f"Erro ao processar mensagem: {error}"
            )
