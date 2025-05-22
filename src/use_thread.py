import asyncio
import threading
from contextlib import suppress

import serial_asyncio


class COMListen(threading.Thread):
    value: str

    def __init__(self, loop, text):
        threading.Thread.__init__(self)
        self._loop = loop
        self._task = None
        self.value = text
        self._writer = None

    def run(self):
        try:
            asyncio.set_event_loop(self._loop)
            self._task = asyncio.ensure_future(self.main())

            self._loop.run_forever()
            self._loop.run_until_complete(self._loop.shutdown_asyncgens())

            self._task.cancel()
            with suppress(asyncio.CancelledError):
                self._loop.run_until_complete(self._task)
        finally:
            self._loop.close()

    def stop(self):
        self._loop.call_soon_threadsafe(self._loop.stop)

    async def send(self, text):
        print(text)
        if self._writer is not None:
            self._writer.write(str(text).encode("utf-8"))
            await self._writer.drain()

    async def read_from_serial(self, reader):
        while True:
            data = await reader.read(100)
            self.value = data.decode()
            print(self.value)

    async def main(self):
        reader, writer = await serial_asyncio.open_serial_connection(url="COM5", baudrate=9600)
        self._writer = writer
        return self._loop.create_task(self.read_from_serial(reader))
