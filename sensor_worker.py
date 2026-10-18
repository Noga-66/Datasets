"""sensor.readings -> يخزن القراءة -> Sensor Agent -> events.perceived لو فيه شذوذ."""
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from backend.agents.sensor_agent import SensorAgent
from backend.contracts.events import Event
from backend.contracts.topics import EVENTS_PERCEIVED, SENSOR_READINGS
from backend.core.kafka import consume, publish
from backend.db.models import Device, SensorReading
from backend.db.session import session_scope

logging.basicConfig(level=logging.INFO)
agent = SensorAgent()
COOLDOWN_MIN = 5
_last_emit: dict[str, datetime] = {}


def handle(msg: dict) -> None:
    ts = datetime.fromisoformat(str(msg["timestamp"]).replace("Z", "+00:00"))
    with session_scope() as s:
        dev = s.get(Device, msg["device_id"])
        if dev is None:
            raise ValueError(f"unknown device {msg['device_id']}")  # -> DLQ
        dev.last_seen = datetime.now(timezone.utc)
        window = list(s.scalars(
            select(SensorReading.value).where(
                SensorReading.device_id == dev.id,
                SensorReading.ts >= ts - timedelta(minutes=5)).order_by(SensorReading.ts.desc()).limit(120)))
        s.add(SensorReading(device_id=dev.id, sensor_type=msg["sensor_type"], value=msg["value"], ts=ts))
        res = agent.run(msg["sensor_type"], msg["value"], window)
        if not res:
            return
        last = _last_emit.get(dev.id)
        if last and datetime.now(timezone.utc) - last < timedelta(minutes=COOLDOWN_MIN):
            return  # ما نغرقش الـ pipeline بنفس الشذوذ
        _last_emit[dev.id] = datetime.now(timezone.utc)
        itype, conf = res
        ev = Event(source="sensor", type=itype, confidence=conf, lat=dev.lat, lon=dev.lon,
                   timestamp=ts, device_id=dev.id,
                   payload={"sensor_type": msg["sensor_type"], "value": msg["value"]})
        publish(EVENTS_PERCEIVED, ev.model_dump(mode="json"), key=dev.id)


if __name__ == "__main__":
    consume([SENSOR_READINGS], "sensor_worker", handle)
