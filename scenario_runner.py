"""سيناريو تسرب مياه: حساس -> بلاغ مواطن. (الكاميرا: camera_simulator يرفع صورة لو متاحة)
python simulation/scenario_runner.py --api http://localhost:8000 --scenario water_leak"""
import argparse, subprocess, sys, time
import requests

p = argparse.ArgumentParser()
p.add_argument("--api", default="http://localhost:8000"); p.add_argument("--scenario", default="water_leak")
p.add_argument("--citizen", default="citizen1"); p.add_argument("--password", default="ChangeMe123!")
p.add_argument("--lat", type=float, default=30.1200); p.add_argument("--lon", type=float, default=31.2500)
a = p.parse_args()

print("1) sensor abnormal ...")
subprocess.Popen([sys.executable, "simulation/sensor_simulator.py", "--mode", "abnormal", "--n", "30"]).wait()
time.sleep(3)
print("2) citizen report ...")
tok = requests.post(f"{a.api}/auth/login", json={"username": a.citizen, "password": a.password}).json()["access_token"]
r = requests.post(f"{a.api}/events/report", headers={"Authorization": f"Bearer {tok}"},
                  data={"text": "في تسريب مياه كبير من ماسورة في الشارع", "lat": a.lat, "lon": a.lon})
print(r.status_code, r.json())
print("افتحي /incidents أو Swagger على", a.api + "/docs", "وشوفي الحادث: المصدران لازم يبقوا في حادث واحد.")
