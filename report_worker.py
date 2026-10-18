"""citizen.reports -> Report Agent (النص) -> events.perceived."""
import logging
from datetime import datetime, timezone
from backend.agents.report_agent import ReportAgent
from backend.contracts.events import Event
from backend.contracts.topics import CITIZEN_REPORTS, EVENTS_PERCEIVED
from backend.core.kafka import consume, publish

logging.basicConfig(level=logging.INFO)
agent = ReportAgent()


def handle(msg: dict) -> None:
    r = agent.run(msg["text"])
    ev = Event(id=msg["event_id"], source="report", type=r["type"], confidence=r["confidence"],
               lat=msg["lat"], lon=msg["lon"], timestamp=datetime.now(timezone.utc),
               object_key=msg.get("object_key"),
               payload={"user_id": msg.get("user_id"), "text": msg["text"], "urgency": r["urgency"]})
    publish(EVENTS_PERCEIVED, ev.model_dump(mode="json"), key=msg["event_id"])


if __name__ == "__main__":
    consume([CITIZEN_REPORTS], "report_worker", handle)
