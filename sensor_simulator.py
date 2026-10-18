"""ينشر على MQTT بنفس شكل الـ ESP32 بالظبط.
python simulation/sensor_simulator.py --mode abnormal --device water_01"""
import argparse, json, random, time
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

p = argparse.ArgumentParser()
p.add_argument("--host", default="localhost"); p.add_argument("--port", type=int, default=1883)
p.add_argument("--user", default="simulator"); p.add_argument("--password", default="")
p.add_argument("--device", default="water_01"); p.add_argument("--type", default="water_flow")
p.add_argument("--mode", choices=["normal", "abnormal"], default="normal")
p.add_argument("--n", type=int, default=40); p.add_argument("--interval", type=float, default=0.5)
a = p.parse_args()

c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
c.username_pw_set(a.user, a.password); c.connect(a.host, a.port); c.loop_start()
for i in range(a.n):
    base = random.gauss(3.0, 0.3)               # قراءة طبيعية (L/min) - عدّليها بعد الـ calibration
    value = base + (14 if a.mode == "abnormal" and i >= a.n // 2 else 0)
    c.publish(f"city/sensors/{a.device}", json.dumps({
        "device_id": a.device, "sensor_type": a.type, "value": round(value, 2), "unit": "L/min",
        "timestamp": datetime.now(timezone.utc).isoformat()}))
    time.sleep(a.interval)
print("done")
