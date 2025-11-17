from src.engine.base_engine import BaseEngine
import cv2


class RTSPCameraEngine(BaseEngine):
    def __init__(self, rtsp_url: str, model_path: str, skip_frames: int = 3):
        super().__init__(model_path=model_path, skip_frames=skip_frames)
        self.rtsp_url = rtsp_url

    def _open_stream(self):
        return cv2.VideoCapture(self.rtsp_url)
