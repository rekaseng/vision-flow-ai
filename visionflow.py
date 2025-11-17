import argparse
import sys
from PySide6.QtWidgets import QApplication

from src.gui.single_camera_window import SingleCameraWindow
from src.gui.multi_camera_window import MultiCameraWindow
from src.websocket.server import start_websocket_server
from src.engine.single_rtsp_engine import SingleCameraEngine
from src.engine.rtsp_engine import RTSPCameraEngine
from src.utils.logger import logger


def parse_args():
    parser = argparse.ArgumentParser(description="VisionFlow — Realtime YOLO & WebSocket Pipeline")

    parser.add_argument("--single", action="store_true", help="Run single camera GUI mode")
    parser.add_argument("--multi", action="store_true", help="Run multi-camera GUI mode")
    parser.add_argument("--ws", action="store_true", help="Start WebSocket server")
    parser.add_argument("--model", type=str, default="best.pt", help="Path to model file")
    parser.add_argument("--rtsp", type=str, default=None, help="RTSP URL for single camera")
    parser.add_argument("--rtsp-list", nargs="+", help="List of RTSP URLs for multi-camera mode")

    return parser.parse_args()


def run_single_camera(args):
    if not args.rtsp:
        logger.error("Error: --rtsp is required for --single mode")
        sys.exit(1)

    logger.info(f"Launching single camera GUI for: {args.rtsp}")
    engine = SingleCameraEngine(args.rtsp, args.model)

    # Start WebSocket server if requested
    if args.ws:
        start_websocket_server(engine)

    app = QApplication(sys.argv)
    window = SingleCameraWindow(args.rtsp, args.model)
    window.show()
    sys.exit(app.exec())


def run_multi_camera(args):
    if not args.rtsp_list:
        logger.error("Error: --rtsp-list is required for --multi mode")
        sys.exit(1)

    logger.info(f"Launching multi-camera GUI with {len(args.rtsp_list)} streams")
    engines = [RTSPCameraEngine(url, args.model) for url in args.rtsp_list]

    # If WebSocket mode enabled → use only first engine for WS API
    if args.ws:
        start_websocket_server(engines[0])

    app = QApplication(sys.argv)
    window = MultiCameraWindow(args.rtsp_list, args.model)
    window.show()
    sys.exit(app.exec())


def run_ws_only(args):
    if not args.rtsp:
        logger.error("Error: --rtsp is required for --ws-only mode")
        sys.exit(1)

    logger.info("Running headless WebSocket engine mode.")
    engine = SingleCameraEngine(args.rtsp, args.model)
    start_websocket_server(engine)

    engine.start()
    logger.info("Engine started. WebSocket running.")

    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        engine.stop()


if __name__ == "__main__":
    args = parse_args()

    if args.single:
        run_single_camera(args)

    elif args.multi:
        run_multi_camera(args)

    elif args.ws:
        run_ws_only(args)

    else:
        print("""
Usage:
  python visionflow.py --single --rtsp rtsp://...
  python visionflow.py --single --rtsp rtsp://... --ws
  python visionflow.py --multi --rtsp-list cam1 cam2 --ws
  python visionflow.py --ws --rtsp rtsp://...
""")
