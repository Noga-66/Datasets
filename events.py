"""العقود المشتركة. أي تغيير هنا بيأثر على كل الفريق."""
from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from uuid import uuid4
from pydantic import BaseModel, Field


class IncidentStatus(str, Enum):  # نفس حالات البروبوزال + REOPENED
    DETECTED = "DETECTED"
    ANALYZED = "ANALYZED"
    FUSED = "FUSED"
    PRIORITIZED = "PRIORITIZED"
    ASSIGNED = "ASSIGNED"
    RESOLVED = "RESOLVED"
    VERIFIED = "VERIFIED"
    REOPENED = "REOPENED"


class IncidentType(str, Enum):
    WATER_LEAK = "water_leak"
    FIRE_SMOKE = "fire_smoke"
    GARBAGE = "garbage"
    POTHOLE = "pothole"
    OTHER = "other"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Event(BaseModel):
    """دليل واحد من مصدر واحد (camera / sensor / report)."""
    schema_version: int = 1
    id: str = Field(default_factory=lambda: uuid4().hex)
    source: Literal["camera", "sensor", "report"]
    type: IncidentType
    confidence: float = Field(ge=0, le=1)
    lat: float
    lon: float
    timestamp: datetime = Field(default_factory=_now)
    device_id: str | None = None
    object_key: str | None = None  # الصورة في MinIO
    payload: dict[str, Any] = {}


class GeoContext(BaseModel):
    nearest: dict[str, dict] = {}   # kind -> {name, distance_m}
    sensitive_distance_m: float | None = None


class FusionResult(BaseModel):
    action: Literal["merge", "create"]
    incident_id: str | None = None
    match_score: float = 0.0
    reasons: list[str] = []


class PriorityResult(BaseModel):
    level: Priority
    score: float
    breakdown: dict[str, float]


class RoutingResult(BaseModel):
    department_code: str | None
    reason: str
    source: Literal["table", "rag", "none"] = "table"
