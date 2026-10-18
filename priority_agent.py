from backend.agents.base import BaseAgent
from backend.config import settings
from backend.contracts.events import GeoContext, IncidentType, Priority, PriorityResult

# أوزان خطورة النوع (افتراضات تحتاج تبرير في التقرير)
TYPE_SEVERITY = {
    IncidentType.FIRE_SMOKE: 1.0,
    IncidentType.WATER_LEAK: 0.6,
    IncidentType.POTHOLE: 0.4,
    IncidentType.GARBAGE: 0.2,
    IncidentType.OTHER: 0.3,
}


def geo_factor(g: GeoContext | None) -> float:
    if not g or g.sensitive_distance_m is None:
        return 0.0
    return 1.0 if g.sensitive_distance_m <= 100 else 0.5 if g.sensitive_distance_m <= 300 else 0.2


def to_level(score: float) -> Priority:
    return (Priority.LOW if score < 0.3 else Priority.MEDIUM if score < 0.55
            else Priority.HIGH if score < 0.8 else Priority.CRITICAL)


class PriorityAgent(BaseAgent):
    name = "priority"

    def run(self, itype: IncidentType, geo: GeoContext | None, n_sources: int,
            confidences: list[float]) -> PriorityResult:
        parts = {
            "type": settings.prio_w_type * TYPE_SEVERITY[itype],
            "geo": settings.prio_w_geo * geo_factor(geo),
            "sources": settings.prio_w_sources * min(1.0, n_sources / 3),
            "confidence": settings.prio_w_conf * (sum(confidences) / len(confidences) if confidences else 0),
        }
        score = round(sum(parts.values()), 3)
        level = to_level(score)
        # override: حريق بثقة عالية = Critical مباشرة
        if itype == IncidentType.FIRE_SMOKE and confidences and max(confidences) >= 0.8:
            level = Priority.CRITICAL
        return PriorityResult(level=level, score=score, breakdown={k: round(v, 3) for k, v in parts.items()})
