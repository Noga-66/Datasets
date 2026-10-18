"""incidents.updates -> أوامر LED على MQTT. (الـ WebSocket بيتغذى من الـ API نفسه.)"""
import json
import logging
import paho.mqtt.client as mqtt
from backend.config import settings
from backend.contracts.topics import INCIDENTS_UPDATES
from backend.core.kafka import consume

logging.basicConfig(level=logging.INFO)
COLOR = {"low": "green", "medium": "yellow", "high": "orange", "critical": "red"}
mq = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


def handle(msg: dict) -> None:
    color = COLOR.get(msg.get("priority") or "", "off")
    mq.publish("city/leds/status", json.dumps({"incident_id": msg["incident_id"], "color": color}))


if __name__ == "__main__":
    mq.username_pw_set(settings.mqtt_user, settings.mqtt_password)
    mq.connect(settings.mqtt_host, settings.mqtt_port)
    mq.loop_start()
    consume([INCIDENTS_UPDATES], "notifier_worker", handle)
