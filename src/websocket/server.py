# vision-flow/src/websocket/server.py

import asyncio
import websockets
import functools
from threading import Thread
from src.websocket.handlers import handle_message
from src.utils.logger import logger


async def client_handler(websocket, engine):
    """
    Each connected client interacts with the engine.
    """
    async for message in websocket:
        response = await handle_message(message, engine)
        await websocket.send(response)


def start_websocket_server(engine, host="0.0.0.0", port=8765):
    """
    Launch WebSocket server in a background thread.
    """

    async def run():
        server = await websockets.serve(
            functools.partial(client_handler, engine=engine),
            host,
            port,
        )
        logger.info(f"WebSocket server running at ws://{host}:{port}")
        await server.wait_closed()

    loop = asyncio.new_event_loop()

    def start_loop():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run())

    t = Thread(target=start_loop, daemon=True)
    t.start()

    return t
