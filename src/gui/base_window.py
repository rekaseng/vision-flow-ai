from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt


class BaseWindow(QWidget):
    """
    Base UI window with a standard white/light theme.
    All windows inherit from this.
    """

    def __init__(self, title: str = "VisionFlow"):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(150, 100, 1100, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #FAFAFA;
                font-family: Segoe UI, Arial;
                font-size: 14px;
                color: #222;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 14px;
                background-color: #FFFFFF;
                border: 1px solid #CCC;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F2F2F2;
            }
        """)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
