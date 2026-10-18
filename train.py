from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolov8n.pt")
    model.train(data="models/vision/dataset.yaml", epochs=50, imgsz=640, project="models/vision", name="run")
    # بعد التدريب: انسخي best.pt إلى models/vision/weights/best.pt
