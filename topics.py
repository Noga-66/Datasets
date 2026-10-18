SENSOR_READINGS = "sensor.readings"
CAMERA_FRAMES = "camera.frames"
CITIZEN_REPORTS = "citizen.reports"
EVENTS_PERCEIVED = "events.perceived"
INCIDENTS_UPDATES = "incidents.updates"
VERIFICATION_REQUESTS = "verification.requests"

ALL_TOPICS = [SENSOR_READINGS, CAMERA_FRAMES, CITIZEN_REPORTS, EVENTS_PERCEIVED,
              INCIDENTS_UPDATES, VERIFICATION_REQUESTS]
DLQ = lambda topic: f"{topic}.dlq"  # noqa: E731

# شكل الرسائل:
# sensor.readings : {device_id, sensor_type, value, unit, timestamp}
# camera.frames   : {event_id, camera_id, object_key, timestamp}
# citizen.reports : {event_id, user_id, text, lat, lon, object_key?, timestamp}
# events.perceived: Event (contracts/events.py)
# incidents.updates: {incident_id, status, priority, department, ...}
# verification.requests: {incident_id, requested_by, timestamp}
