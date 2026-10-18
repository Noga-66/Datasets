"""Mosquitto -> Kafka (sensor.readings). بيتحقق من الرسالة وينسقها."""
import json
import logging
import paho.mqtt.client as mqtt
from backend.config import settings
from backend.contracts.topics import DLQ, SENSOR_READINGS
from backend.core.kafka import publish

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("mqtt_bridge")
REQUIRED = {"device_id", "sensor_type", "value", "timestamp"}


def on_connect(c, userdata, flags, rc, props=None):
    log.info("connected to MQTT (rc=%s)", rc)
    c.subscribe("city/sensors/#")


def on_message(c, userdata, msg):
    try:
        data = json.loads(msg.payload)
        if not REQUIRED <= data.keys():
            raise ValueError(f"missing fields: {REQUIRED - data.keys()}")
        data["value"] = float(data["value"])
        publish(SENSOR_READINGS, data, key=data["device_id"])
    except Exception as exc:  # noqa: BLE001
        log.warning("invalid payload quarantined: %s", exc)
        publish(DLQ(SENSOR_READINGS), {"error": str(exc), "raw": msg.payload.decode(errors="replace")})


def main():
    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    c.username_pw_set(settings.mqtt_user, settings.mqtt_password)
    c.on_connect, c.on_message = on_connect, on_message
    c.reconnect_delay_set(1, 30)
    c.connect(settings.mqtt_host, settings.mqtt_port)
    c.loop_forever()


if __name__ == "__main__":
    main()
