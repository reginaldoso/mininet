import asyncio


class EventManager:

    def __init__(self):
        self.queue = asyncio.Queue()

    async def publish(self, event_type, data=None):
        await self.queue.put({
            "type": event_type,
            "data": data
        })

    async def subscribe(self):
        return await self.queue.get()