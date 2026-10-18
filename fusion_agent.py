from datetime import timedelta
from sqlalchemy.orm import Session
from backend.agents.base import BaseAgent
from backend.config import settings
from backend.contracts.events import Event, FusionResult
from backend.services import geo_service
from datetime import datetime, timezone


def match_score(dist_m: float, dt_min: float, radius_m: float, window_min: float,
                w_space: float, w_time: float) -> float:
    """دالة نقية (بتتختبر لوحدها). النوع المتوافق بيتفلتر قبلها كـ hard gate."""
    s_space = max(0.0, 1 - dist_m / radius_m)
    s_time = max(0.0, 1 - dt_min / window_min)
    total = w_space + w_time
    return (w_space * s_space + w_time * s_time) / total


class FusionAgent(BaseAgent):
    name = "fusion"

    def run(self, s: Session, ev: Event) -> FusionResult:
        if not settings.fusion_enabled:
            return FusionResult(action="create", reasons=["fusion disabled (ablation)"])
        now = datetime.now(timezone.utc)
        since = now - timedelta(minutes=settings.fusion_window_min)
        cands = geo_service.open_incidents_near(
            s, ev.lat, ev.lon, settings.fusion_radius_m, since, ev.type.value)  # hard gate: نفس النوع
        best = None
        for c in cands:
            dt = (now - c["updated_at"]).total_seconds() / 60
            sc = match_score(c["distance_m"], dt, settings.fusion_radius_m,
                             settings.fusion_window_min, settings.fusion_w_space, settings.fusion_w_time)
            if best is None or sc > best[0]:
                best = (sc, c, dt)
        if best and best[0] >= settings.fusion_threshold:
            sc, c, dt = best
            return FusionResult(action="merge", incident_id=c["id"], match_score=round(sc, 2),
                                reasons=[f"distance {c['distance_m']:.0f} m", f"{dt:.0f} min since last update",
                                         f"same type: {ev.type.value}"])
        return FusionResult(action="create", match_score=round(best[0], 2) if best else 0.0,
                            reasons=["no matching open incident"])
