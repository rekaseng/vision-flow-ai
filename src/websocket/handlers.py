import json
from src.websocket.protocol import *
from src.utils.logger import logger


async def handle_message(message: str, engine):
    """
    Process WebSocket messages via W1 protocol.
    """

    msg = message.strip().lower()

    # ========== START ==========
    if msg == CMD_START:
        engine.start()
        return RESPONSE_OK

    # ========== STOP ==========
    elif msg == CMD_STOP:
        engine.stop()
        return RESPONSE_OK

    # ========== RETURN DETECTIONS ==========
    elif msg.startswith(CMD_DETECTIONS):
        det = engine.last_detection or {"detections": [], "timestamp": None}
        return json.dumps(det)

    # ========== UNKNOWN ==========
    else:
        logger.warning(f"Unknown command: {msg}")
        return json.dumps({
            "status": RESPONSE_ERROR,
            "message": "unknown command"
        })
