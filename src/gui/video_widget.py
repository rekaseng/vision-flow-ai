# vision-flow/src/gui/video_widget.py

import cv2
import numpy as np
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt


class VideoWidget(QLabel):
    """
    A QLabel that displays frames from an engine.
    """

    def __init__(self, width=640, height=360):
        super().__init__("No Feed")
        self.setFixedSize(width, height)
        self.setAlignment(Qt.AlignCenter)

    def update_frame(self, frame: np.ndarray):
        """Convert CV2 frame → QImage → display."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w

        qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)

        self.setPixmap(pixmap)
