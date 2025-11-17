import threading
import queue
import time
import cv2
from typing import Optional, Any, Dict, List
from src.models.model_loader import VisionFlowModel
from src.utils.logger import logger
from datetime import datetime


class BaseEngine:
    """
    Base class for:
    - RTSP Engines
    - Video File Engines
    - Multi-camera engines

    Handles:
    - Thread lifecycle
    - Frame skipping
    - Prediction pipeline
    - Shared detection state
    """

    def __init__(self, model_path: str, skip_frames: int = 3, queue_size: int = 10):
        self.model = VisionFlowModel(model_path)
        self.skip_frames = skip_frames

        self.frame_counter = 0
        self.queue = queue.Queue(maxsize=queue_size)

        self.running = False
        self.last_detection: Optional[List[Dict[str, Any]]] = None

    # --------------------- THREAD CONTROL ---------------------

    def start(self):
        if self.running:
            return

        self.running = True
        self.recv_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self.pred_thread = threading.Thread(target=self._predict_loop, daemon=True)

        self.recv_thread.start()
        self.pred_thread.start()

        logger.info(f"{self.__class__.__name__} started.")

    def stop(self):
        self.running = False
        logger.info(f"{self.__class__.__name__} stopped.")

    # --------------------- ABSTRACT ---------------------

    def _open_stream(self):
        """Implement in subclass: return cv2.VideoCapture instance."""
        raise NotImplementedError

    # --------------------- INTERNAL LOOPS ---------------------

    def _receive_loop(self):
        cap = self._open_stream()

        if cap is None or not cap.isOpened():
            logger.error("Failed to open stream.")
            return

        while self.running:
            ret, frame = cap.read()
            if not ret:
                logger.warning("Frame read failed. Attempting reconnect...")
                time.sleep(1)
                cap = self._open_stream()
                continue

            if not self.queue.full():
                self.queue.put(frame)

        cap.release()

    def _predict_loop(self):
        while self.running:
            if self.queue.empty():
                time.sleep(0.01)
                continue

            frame = self.queue.get()

            self.frame_counter += 1
            if self.frame_counter % self.skip_frames != 0:
                continue

            detections = self.model.predict(frame)

            self.last_detection = {
                "timestamp": datetime.utcnow().isoformat(),
                "detections": detections
            }
