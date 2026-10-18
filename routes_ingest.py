from uuid import uuid4
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from backend.contracts.topics import CAMERA_FRAMES, CITIZEN_REPORTS
from backend.core import storage
from backend.core.deps import require_role
from backend.core.kafka import publish

router = APIRouter(prefix="/events", tags=["ingest"])
MAX_BYTES = 5 * 1024 * 1024
ALLOWED = {"image/jpeg", "image/png"}


async def _read_image(f: UploadFile) -> bytes:
    if f.content_type not in ALLOWED:
        raise HTTPException(415, "only jpeg/png")
    data = await f.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "image too large")
    return data


@router.post("/camera", status_code=202)
async def camera(camera_id: str = Form(...), image: UploadFile = File(...),
                 user: dict = Depends(require_role("device"))):
    key = storage.upload("camera-frames", await _read_image(image))
    publish(CAMERA_FRAMES, {"event_id": uuid4().hex, "camera_id": camera_id, "object_key": key,
                            "timestamp": datetime.now(timezone.utc).isoformat()}, key=camera_id)
    return {"object_key": key}


@router.post("/report", status_code=202)
async def report(text: str = Form(..., max_length=2000), lat: float = Form(..., ge=-90, le=90),
                 lon: float = Form(..., ge=-180, le=180), image: UploadFile | None = File(None),
                 user: dict = Depends(require_role("citizen"))):
    key = storage.upload("citizen-reports", await _read_image(image)) if image else None
    eid = uuid4().hex
    publish(CITIZEN_REPORTS, {"event_id": eid, "user_id": user["sub"], "text": text, "lat": lat,
                              "lon": lon, "object_key": key,
                              "timestamp": datetime.now(timezone.utc).isoformat()}, key=eid)
    return {"event_id": eid}
