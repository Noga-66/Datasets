"""Raspberry Pi: يلتقط صورة كل N ثانية ويرفعها للـ API بـ Device JWT.
pip install requests opencv-python"""
import os, time
import cv2, requests

API = os.environ.get("API", "http://localhost:8000")
TOKEN = os.environ["DEVICE_JWT"]        # من POST /auth/login بيوزر الجهاز
CAMERA_ID = os.environ.get("CAMERA_ID", "cam_01")
INTERVAL = float(os.environ.get("INTERVAL", 5))

cap = cv2.VideoCapture(0)
while True:
    ok, frame = cap.read()
    if ok:
        _, buf = cv2.imencode(".jpg", frame)
        r = requests.post(f"{API}/events/camera", headers={"Authorization": f"Bearer {TOKEN}"},
                          data={"camera_id": CAMERA_ID}, files={"image": ("f.jpg", buf.tobytes(), "image/jpeg")})
        print(r.status_code)
    time.sleep(INTERVAL)
