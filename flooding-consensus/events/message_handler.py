from communication.message import Message ## determinar a função da classe Message neste código


class MessageHandler:

    def __init__(self, node): ## self guarda o ConsensusNode ao qual o gestor de mensagem pertence
        self.node = node

    async def handle(self, data):## gerir mensagens enviadas aos nós vizinhos

        try:
            message = Message.deserialize(data)

            self.node.metrics.register_received() ## falta implementar função que vai contabilizar msgs recebidas

            if message.sender == self.node.process_id:
                return

            if message.round_number > self.node.round_number:
                return ## isto está errado. Precisa corrigir

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
