"""camera.frames -> تنزيل الصورة من MinIO -> YOLO -> events.perceived."""
import logging
from datetime import datetime, timezone
from backend.agents.vision_agent import VisionAgent
from backend.contracts.events import Event
from backend.contracts.topics import CAMERA_FRAMES, EVENTS_PERCEIVED
from backend.core.kafka import consume, publish
from backend.core.storage import download
from backend.db.models import Device
from backend.db.session import session_scope

logging.basicConfig(level=logging.INFO)
agent = VisionAgent()


def handle(msg: dict) -> None:
    with session_scope() as s:
        cam = s.get(Device, msg["camera_id"])
        if cam is None:
            raise ValueError(f"unknown camera {msg['camera_id']}")
        lat, lon = cam.lat, cam.lon
    for det in agent.run(download(msg["object_key"])):
        ev = Event(source="camera", type=det["type"], confidence=det["confidence"], lat=lat, lon=lon,
                   timestamp=datetime.now(timezone.utc), device_id=msg["camera_id"],
                   object_key=msg["object_key"], payload={"bbox": det["bbox"]})
        publish(EVENTS_PERCEIVED, ev.model_dump(mode="json"), key=msg["camera_id"])


if __name__ == "__main__":
    consume([CAMERA_FRAMES], "vision_worker", handle)
