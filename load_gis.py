"""يحمّل مدارس/مستشفيات... من GeoJSON (مستخرج من OSM) لجدول places.
مثال استخراج من Overpass:  node/way[amenity=school|hospital|fire_station|police] داخل bbox
الاستخدام: python -m backend.scripts.load_gis data/gis/places.geojson"""
import json
import sys
from backend.db.models import Place
from backend.db.session import session_scope

KIND_MAP = {"school": "school", "hospital": "hospital", "fire_station": "fire_station", "police": "police"}

if __name__ == "__main__":
    path = sys.argv[1]
    n = 0
    with session_scope() as s:
        for f in json.load(open(path, encoding="utf-8"))["features"]:
            kind = KIND_MAP.get(f["properties"].get("amenity"))
            geom = f["geometry"]
            if not kind or geom["type"] != "Point":
                continue
            lon, lat = geom["coordinates"]
            s.add(Place(kind=kind, name=f["properties"].get("name", ""), lat=lat, lon=lon)); n += 1
    print(f"loaded {n} places")
