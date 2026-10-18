"""بيانات أولية: إدارات + مستخدمين + أجهزة. غيّري الإحداثيات لموقع المجسم/الجامعة."""
import os
from backend.core.security import hash_password
from backend.db.models import Department, Device, User
from backend.db.session import session_scope

BASE_LAT, BASE_LON = 30.1200, 31.2500   # TODO: غيّريها لموقعك الحقيقي

DEPTS = [("water", "Water & Sewage", ["water_leak"]), ("civil_defense", "Civil Defense", ["fire_smoke"]),
         ("sanitation", "Sanitation", ["garbage"]), ("roads", "Roads Maintenance", ["pothole"])]
USERS = [("operator1", "operator", None), ("water_staff", "department", "water"),
         ("cam_01", "device", None), ("citizen1", "citizen", None)]
DEVICES = [("water_01", "sensor", "water_flow", 0.0, 0.0), ("smoke_01", "sensor", "smoke", 0.0003, 0.0003),
           ("cam_01", "camera", None, 0.00005, 0.00005)]

if __name__ == "__main__":
    pw = os.environ.get("SEED_PASSWORD", "ChangeMe123!")
    with session_scope() as s:
        for code, name, handles in DEPTS:
            s.merge(Department(code=code, name=name, handles=handles))
        for u, role, dept in USERS:
            s.merge(User(id=u, username=u, password_hash=hash_password(pw), role=role, department_code=dept))
        for d, kind, st, dlat, dlon in DEVICES:
            s.merge(Device(id=d, kind=kind, sensor_type=st, lat=BASE_LAT + dlat, lon=BASE_LON + dlon))
    print("seeded. default password from SEED_PASSWORD (غيّريه!)")
