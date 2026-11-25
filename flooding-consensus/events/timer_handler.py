import asyncio


class TimerHandler:

    @staticmethod
    async def wait(seconds):
        await asyncio.sleep(seconds)

    @staticmethod
    async def wait_for_event(event, timeout):

        try:
            return await asyncio.wait_for(
                event,
                timeout=timeout
            )

        except asyncio.TimeoutError:
            return None
