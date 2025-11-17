import numpy as np
import cv2
from ultralytics import YOLO
from src.models.sku_map import normalize_label, SKU_MAP
from src.utils.logger import logger
from src.config.settings import settings
from typing import Dict, Any


class VisionFlowModel:
    """
    Wrapper model that automatically supports:
    - YOLOv8 .pt
    - TFLite (EdgeTPU or CPU)
    """

    def __init__(self, model_path: str = None):
        self.model_path = model_path or settings.model.default_model

        if model_path.endswith(".tflite"):
            self.backend = "tflite"
            self._load_tflite(model_path)
        else:
            self.backend = "yolo"
            self._load_yolo(model_path)

        logger.info(f"Loaded model ({self.backend}): {self.model_path}")

    # ----------------- YOLO MODEL -----------------

    def _load_yolo(self, path):
        self.model = YOLO(path)

    # ---------------- TFLITE MODEL ----------------

    def _load_tflite(self, path):
        import tflite_runtime.interpreter as tflite

        self.interpreter = tflite.Interpreter(model_path=path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        input_shape = self.input_details[0]["shape"]
        self.input_height = input_shape[1]
        self.input_width = input_shape[2]

    # ------------- PUBLIC PREDICT -----------------

    def predict(self, frame) -> Dict[str, Any]:
        if self.backend == "yolo":
            return self._predict_yolo(frame)
        return self._predict_tflite(frame)

    # ------------- YOLO PREDICT -------------------

    def _predict_yolo(self, frame):
        results = self.model(frame)[0]
        detections = []

        for box in results.boxes:
            cls_id = int(box.cls)
            label = results.names[cls_id]
            confidence = float(box.conf)
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            label_norm = normalize_label(label)
            sku = SKU_MAP.get(label_norm)

            detections.append({
                "label": label_norm,
                "confidence": confidence,
                "sku": sku,
                "bbox": {
                    "left": x1,
                    "top": y1,
                    "right": x2,
                    "bottom": y2
                }
            })

        return detections

    # ------------- TFLITE PREDICT -----------------

    def _predict_tflite(self, frame):
        img = cv2.resize(frame, (self.input_width, self.input_height))
        img = np.expand_dims(img, axis=0)
        img = img.astype(np.uint8)

        self.interpreter.set_tensor(self.input_details[0]["index"], img)
        self.interpreter.invoke()

        output = self.interpreter.get_tensor(self.output_details[0]["index"])

        detections = []
        for det in output:
            x1, y1, x2, y2, conf, cls = det
            label = normalize_label(cls)
            sku = SKU_MAP.get(label)

            detections.append({
                "label": label,
                "confidence": float(conf),
                "sku": sku,
                "bbox": {
                    "left": float(x1),
                    "top": float(y1),
                    "right": float(x2),
                    "bottom": float(y2),
                }
            })

        return detections
