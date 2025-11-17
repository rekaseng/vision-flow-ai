import cv2
import os
from ultralytics import YOLO
from .cvat_writer import CVATWriter


def export_video_to_cvat(video_path, model_path, output_dir, skip_frames=1):
    """
    Basic CVAT export:
    - Runs YOLO on each frame
    - Writes per-frame <image> with <box> entries
    - No tracking, no interpolation
    """

    model = YOLO(model_path)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_file = os.path.join(output_dir, f"{video_name}.xml")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"[CVAT Export] Processing: {video_path}")
    print(f"[CVAT Export] Total frames: {total_frames}")

    writer = CVATWriter(width=width, height=height)

    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % skip_frames != 0:
            frame_index += 1
            continue

        results = model(frame)

        boxes = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                cls = result.names[int(box.cls)]
                conf = float(box.conf)

                boxes.append({
                    "label": cls,
                    "xtl": x1,
                    "ytl": y1,
                    "xbr": x2,
                    "ybr": y2,
                    "confidence": conf
                })

        writer.add_frame(frame_index, boxes)
        frame_index += 1

    cap.release()

    writer.save(output_file)
    print(f"[CVAT Export] Saved: {output_file}")
