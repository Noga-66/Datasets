"""verification.requests -> فحوصات قبل/بعد -> VERIFIED أو REOPENED."""
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from backend.agents.verification_agent import VerificationAgent
from backend.contracts.events import IncidentStatus as S
from backend.contracts.topics import INCIDENTS_UPDATES, VERIFICATION_REQUESTS
from backend.core.kafka import consume, publish
from backend.db.models import Incident, SensorReading
from backend.db.session import session_scope
from backend.services import incident_service as svc

logging.basicConfig(level=logging.INFO)
agent = VerificationAgent()
NORMAL_MAX = {"water_flow": 5.0, "smoke": 100.0, "gas": 100.0}  # من الـ calibration
STABLE_MIN = 3


def sensor_check(s, inc) -> bool | None:
    """الحساس رجع للنطاق الطبيعي لآخر STABLE_MIN دقايق؟ None = مفيش حساس/قراءات."""
    dev_ids = {e.device_id for e in inc.events if e.source == "sensor" and e.device_id}
    if not dev_ids:
        return None
    since = datetime.now(timezone.utc) - timedelta(minutes=STABLE_MIN)
    rows = list(s.scalars(select(SensorReading).where(SensorReading.device_id.in_(dev_ids),
                                                      SensorReading.ts >= since)))
    if not rows:
        return None
    return all(r.value <= NORMAL_MAX.get(r.sensor_type, float("inf")) for r in rows)


def vision_check(s, inc) -> bool | None:
    # TODO: صورة جديدة من نفس الكاميرا -> VisionAgent -> هل لسه بيكتشف نفس النوع؟ (+ SSIM قبل/بعد)
    return None


def handle(msg: dict) -> None:
    with session_scope() as s:
        inc = s.get(Incident, msg["incident_id"])
        if inc is None or inc.status != S.RESOLVED.value:
            return
        ok, notes = agent.run({"sensor": sensor_check(s, inc), "vision": vision_check(s, inc)})
        if ok:
            svc.advance(s, inc, S.VERIFIED, "agent:verification", "; ".join(notes))
        else:
            svc.advance(s, inc, S.REOPENED, "agent:verification", "; ".join(notes))
            svc.advance(s, inc, S.ASSIGNED, "agent:routing", "re-assigned after failed verification")
        s.flush()
        publish(INCIDENTS_UPDATES, {"incident_id": inc.id, "type": inc.type, "status": inc.status,
                                    "priority": inc.priority, "department": inc.department_code,
                                    "lat": inc.lat, "lon": inc.lon}, key=inc.id)


if __name__ == "__main__":
    consume([VERIFICATION_REQUESTS], "verification_worker", handle)
