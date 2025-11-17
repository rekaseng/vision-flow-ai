from src.engine.base_engine import BaseEngine
import cv2
from src.utils.logger import logger


class VideoFileEngine(BaseEngine):
    def __init__(self, file_path: str, model_path: str, skip_frames: int = 3):
        super().__init__(model_path=model_path, skip_frames=skip_frames)
        self.file_path = file_path

    def _open_stream(self):
        logger.info(f"Opening video file: {self.file_path}")
        return cv2.VideoCapture(self.file_path)
