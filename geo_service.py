"""استعلامات PostGIS على lat/lon (geography => المسافات بالمتر)."""
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session

_PT = "ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography"


def nearest_places(s: Session, lat: float, lon: float, kinds: list[str], radius_m: float = 500) -> list[dict]:
    rows = s.execute(text(f"""
        SELECT DISTINCT ON (kind) kind, name,
               ST_Distance(ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography, {_PT}) AS d
        FROM places
        WHERE kind = ANY(:kinds)
          AND ST_DWithin(ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography, {_PT}, :r)
        ORDER BY kind, d
    """), {"lat": lat, "lon": lon, "kinds": kinds, "r": radius_m}).all()
    return [{"kind": r.kind, "name": r.name, "distance_m": round(r.d, 1)} for r in rows]


def open_incidents_near(s: Session, lat: float, lon: float, radius_m: float,
                        since: datetime, inc_type: str) -> list[dict]:
    rows = s.execute(text(f"""
        SELECT id, created_at, updated_at,
               ST_Distance(ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography, {_PT}) AS d
        FROM incidents
        WHERE type = :t AND status <> 'VERIFIED' AND updated_at >= :since
          AND ST_DWithin(ST_SetSRID(ST_MakePoint(lon, lat), 4326)::geography, {_PT}, :r)
        ORDER BY d
    """), {"lat": lat, "lon": lon, "t": inc_type, "since": since, "r": radius_m}).all()
    return [{"id": r.id, "distance_m": r.d, "updated_at": r.updated_at} for r in rows]
