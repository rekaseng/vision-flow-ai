import threading
import time
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QLabel

from src.gui.base_window import BaseWindow
from src.gui.video_widget import VideoWidget
from src.engine.rtsp_engine import RTSPCameraEngine


class MultiCameraWindow(BaseWindow):
    """
    UI for multiple RTSP feeds (2–4 cameras).
    """

    def __init__(self, camera_urls: list, model_path: str):
        super().__init__("VisionFlow – Multi Camera")

        self.engines = []
        self.widgets = []

        for url in camera_urls:
            self.engines.append(RTSPCameraEngine(url, model_path, skip_frames=3))

        hlayout = QHBoxLayout()
        for _ in camera_urls:
            vw = VideoWidget(480, 320)
            self.widgets.append(vw)
            hlayout.addWidget(vw)

        self.layout.addLayout(hlayout)

        # Buttons
        btn = QPushButton("Start All")
        btn2 = QPushButton("Stop All")
        self.layout.addWidget(btn)
        self.layout.addWidget(btn2)

        btn.clicked.connect(self.start_all)
        btn2.clicked.connect(self.stop_all)

        self.running_ui = False

    def start_all(self):
        for e in self.engines:
            e.start()
        self.running_ui = True

        threading.Thread(target=self.update_loop, daemon=True).start()

    def stop_all(self):
        self.running_ui = False
        for e in self.engines:
            e.stop()

    def update_loop(self):
        while self.running_ui:
            for e, w in zip(self.engines, self.widgets):
                if e.model.last_output and "frame" in e.model.last_output:
                    w.update_frame(e.model.last_output["frame"])
            time.sleep(0.01)
