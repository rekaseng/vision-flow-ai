# VisionFlow  
### Realtime Multi-Camera Computer Vision Pipeline (YOLO + RTSP + WebSocket)

VisionFlow is a unified, production-ready vision system designed for realtime detection, tracking, annotation export, and automated downstream processing.  
It supports **YOLO-based video detection**, **multi-camera RTSP streaming**, **WebSocket integrations**, and **auto-annotation export to CVAT** — all inside a clean, modular architecture.

VisionFlow is optimized for:
- Smart retail & vending machine analytics  
- Automated SKU detection pipelines  
- Edge-device & Raspberry Pi deployments  
- High-speed multi-camera processing  
- Video → XML annotation generation for training  

## 📚 Further Reading & Documentation

For internal design notes, project specs, UI wireframes, and pipeline diagrams, refer to our master documentation file:
[VisionFlow Design & Spec (Coda Doc)](https://coda.io/d/_dxWo56umkwI/VisionFlow_suPDYi1Y)

---

## 🚀 Key Features

### **1. Realtime YOLO Detection**
- Single or multi-camera support  
- RTSP, IP cams, MP4 input  
- Adjustable frame skipping for speed  
- Clean GUI for debugging & demos  

### **2. WebSocket API for Automation**
- Stream detection JSON  
- Live SKU mapping  
- Trigger events from backend  
- Compatible with Node / Python / FastAPI / n8n  

### **3. CVAT Annotation Export**
- Auto-convert YOLO detections → CVAT XML  
- Track-based interpolation  
- Perfect for dataset creation  

### **4. Hybrid Runtime Modes**
Run VisionFlow in any mode:
```bash
# Single camera GUI
python visionflow.py --single --rtsp rtsp://camera

# Single camera + WebSocket
python visionflow.py --single --rtsp rtsp://camera --ws

# Multi-camera GUI
python visionflow.py --multi --rtsp-list cam1 cam2

# Multi-camera + WebSocket
python visionflow.py --multi --rtsp-list cam1 cam2 --ws

# Headless backend only (WS)
python visionflow.py --ws --rtsp rtsp://camera
