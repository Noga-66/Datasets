from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _id() -> str:
    return uuid4().hex


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_id)
    username: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)  # citizen|department|operator|admin|device
    department_code: Mapped[str | None] = mapped_column(String, nullable=True)


class Device(Base):
    __tablename__ = "devices"
    id: Mapped[str] = mapped_column(String, primary_key=True)  # water_01 / cam_01
    kind: Mapped[str] = mapped_column(String)  # sensor|camera
    sensor_type: Mapped[str | None] = mapped_column(String, nullable=True)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Department(Base):
    __tablename__ = "departments"
    code: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    handles: Mapped[list] = mapped_column(JSON, default=list)  # أنواع الحوادث


class Place(Base):  # طبقة GIS مبسطة (مدارس، مستشفيات...) من OSM
    __tablename__ = "places"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_id)
    kind: Mapped[str] = mapped_column(String, index=True)  # school|hospital|fire_station|police
    name: Mapped[str] = mapped_column(String, default="")
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)


class SensorReading(Base):
    __tablename__ = "sensor_readings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    device_id: Mapped[str] = mapped_column(String, index=True)
    sensor_type: Mapped[str] = mapped_column(String)
    value: Mapped[float] = mapped_column(Float)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_id)
    type: Mapped[str] = mapped_column(String)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, default="DETECTED", index=True)
    priority: Mapped[str | None] = mapped_column(String, nullable=True)
    priority_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    department_code: Mapped[str | None] = mapped_column(ForeignKey("departments.code"), nullable=True)
    reopen_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)
    reporter_id: Mapped[str | None] = mapped_column(String, nullable=True)

    events: Mapped[list["EventRow"]] = relationship(back_populates="incident")
    timeline: Mapped[list["TimelineEntry"]] = relationship(back_populates="incident", order_by="TimelineEntry.ts")


class EventRow(Base):
    __tablename__ = "events"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    incident_id: Mapped[str | None] = mapped_column(ForeignKey("incidents.id"), nullable=True, index=True)
    source: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    confidence: Mapped[float] = mapped_column(Float)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    device_id: Mapped[str | None] = mapped_column(String, nullable=True)
    object_key: Mapped[str | None] = mapped_column(String, nullable=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    incident: Mapped[Incident | None] = relationship(back_populates="events")


class TimelineEntry(Base):
    __tablename__ = "incident_timeline"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incident_id: Mapped[str] = mapped_column(ForeignKey("incidents.id"), index=True)
    status: Mapped[str] = mapped_column(String)
    actor: Mapped[str] = mapped_column(String)  # agent:fusion / user:ali
    note: Mapped[str] = mapped_column(Text, default="")
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    incident: Mapped[Incident] = relationship(back_populates="timeline")
