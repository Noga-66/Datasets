"""events.perceived -> Fusion -> Geo -> Priority -> Routing. لازم instance واحد."""
import logging
from backend.contracts.events import Event
from backend.contracts.topics import EVENTS_PERCEIVED
from backend.core.kafka import consume
from backend.db.session import session_scope
from backend.services.pipeline import process_event

logging.basicConfig(level=logging.INFO)


def handle(msg: dict) -> None:
    with session_scope() as s:
        process_event(s, Event(**msg))


if __name__ == "__main__":
    consume([EVENTS_PERCEIVED], "pipeline_worker", handle)
