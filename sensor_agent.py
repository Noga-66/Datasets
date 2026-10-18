"""Sensor Agent: thresholds + z-score على نافذة زمنية. القواعد أول، وIsolation Forest لاحقًا."""
import statistics
from backend.agents.base import BaseAgent
from backend.contracts.events import IncidentType

SENSOR_TO_INCIDENT = {
    "water_flow": IncidentType.WATER_LEAK,
    "smoke": IncidentType.FIRE_SMOKE,
    "gas": IncidentType.FIRE_SMOKE,
}
# القيم دي مجرد افتراضات! لازم تتعدل بعد calibration للحساسات الفعلية.
HARD_THRESHOLD = {"water_flow": 12.0, "smoke": 300.0, "gas": 300.0}
MIN_WINDOW = 10
Z_LIMIT = 3.0


class SensorAgent(BaseAgent):
    name = "sensor"

    def run(self, sensor_type: str, current: float, window: list[float]):
        """يرجع (incident_type, confidence) لو فيه شذوذ، وإلا None."""
        itype = SENSOR_TO_INCIDENT.get(sensor_type)
        if itype is None:
            return None
        hard = current >= HARD_THRESHOLD.get(sensor_type, float("inf"))
        z = 0.0
        if len(window) >= MIN_WINDOW:
            sd = statistics.pstdev(window)
            if sd > 1e-6:
                z = (current - statistics.fmean(window)) / sd
        if hard or z >= Z_LIMIT:
            conf = min(1.0, max(z / 6, 0.6 if hard else 0.0))
            return itype, round(conf, 2)
        return None
