from sqlalchemy.orm import Session
from backend.agents.base import BaseAgent
from backend.contracts.events import GeoContext
from backend.services import geo_service

KINDS = ["school", "hospital", "fire_station", "police"]
SENSITIVE = {"school", "hospital"}


class GeoAgent(BaseAgent):
    """بيدي سياق بس ومابياخدش قرارات."""
    name = "geo"

    def run(self, s: Session, lat: float, lon: float) -> GeoContext:
        places = geo_service.nearest_places(s, lat, lon, KINDS, radius_m=500)
        nearest = {p["kind"]: {"name": p["name"], "distance_m": p["distance_m"]} for p in places}
        sens = [v["distance_m"] for k, v in nearest.items() if k in SENSITIVE]
        return GeoContext(nearest=nearest, sensitive_distance_m=min(sens) if sens else None)
