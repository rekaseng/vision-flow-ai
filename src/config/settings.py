from dataclasses import dataclass
from typing import List
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

@dataclass
class StorageConfig:
    gcp_bucket_raw: str = "shake_recordings"
    gcp_bucket_frames: str = "shake_images"
    gcp_bucket_annotations: str = "shake_annotations"
    temp_dir: str = os.path.join(BASE_DIR, "temp")

@dataclass
class ModelConfig:
    default_model: str = os.path.join(BASE_DIR, "models", "best.pt")
    tflite_model: str = os.path.join(BASE_DIR, "models", "edgetpu_quant.tflite")
    skip_frames: int = 3

@dataclass
class RTSPConfig:
    rtsp_streams: List[str] = None

    def __post_init__(self):
        if self.rtsp_streams is None:
            self.rtsp_streams = [
                "rtsp://192.168.0.111/channel=1_stream=0.sdp?real_stream",
                "rtsp://192.168.0.112/channel=1_stream=0.sdp?real_stream"
            ]

@dataclass
class LoggingConfig:
    log_dir: str = os.path.join(BASE_DIR, "logs")
    log_file: str = "visionflow.log"
    retention_days: int = 7

@dataclass
class VisionFlowSettings:
    storage: StorageConfig = StorageConfig()
    model: ModelConfig = ModelConfig()
    rtsp: RTSPConfig = RTSPConfig()
    logging: LoggingConfig = LoggingConfig()


settings = VisionFlowSettings()
