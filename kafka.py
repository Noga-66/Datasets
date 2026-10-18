import json
import logging
from typing import Callable
from confluent_kafka import Consumer, Producer
from backend.config import settings
from backend.contracts.topics import DLQ

log = logging.getLogger("kafka")
_producer: Producer | None = None


def get_producer() -> Producer:
    global _producer
    if _producer is None:
        _producer = Producer({"bootstrap.servers": settings.kafka_bootstrap})
    return _producer


def publish(topic: str, payload: dict, key: str | None = None) -> None:
    p = get_producer()
    p.produce(topic, json.dumps(payload, default=str).encode(), key=key)
    p.flush(5)


def consume(topics: list[str], group: str, handler: Callable[[dict], None]) -> None:
    """Loop دائم: commit بعد المعالجة، والرسائل الفاشلة تروح لـ *.dlq."""
    c = Consumer({
        "bootstrap.servers": settings.kafka_bootstrap,
        "group.id": group,
        "enable.auto.commit": False,
        "auto.offset.reset": "earliest",
    })
    c.subscribe(topics)
    log.info("consuming %s as %s", topics, group)
    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                log.error("kafka error: %s", msg.error())
                continue
            try:
                handler(json.loads(msg.value()))
            except Exception as exc:  # noqa: BLE001
                log.exception("handler failed, sending to DLQ")
                publish(DLQ(msg.topic()), {"error": str(exc), "raw": msg.value().decode(errors="replace")})
            finally:
                c.commit(msg)
    finally:
        c.close()
