"""Report Agent. النسخة دي keyword-based (عربي/عامية/إنجليزي) كـ baseline وfallback.
التحسين: استبدال classify() بـ LLM بـ Structured Output (JSON schema) مع few-shot مصري."""
from backend.agents.base import BaseAgent
from backend.contracts.events import IncidentType

KEYWORDS = {
    IncidentType.WATER_LEAK: ["مياه", "المية", "ماسورة", "تسريب", "تسرب", "غرق", "leak", "water", "pipe"],
    IncidentType.FIRE_SMOKE: ["حريق", "دخان", "نار", "ريحة غاز", "غاز", "fire", "smoke", "gas"],
    IncidentType.GARBAGE: ["زبالة", "قمامة", "قمامه", "مخلفات", "garbage", "trash", "waste"],
    IncidentType.POTHOLE: ["حفرة", "حفره", "الطريق بايظ", "كسر في الأسفلت", "pothole", "road damage"],
}
URGENT = ["خطر", "عاجل", "الحقوا", "مصابين", "urgent", "danger", "emergency"]


class ReportAgent(BaseAgent):
    name = "report"

    def run(self, text: str) -> dict:
        t = text.lower()
        scores = {k: sum(w in t for w in v) for k, v in KEYWORDS.items()}
        best, hits = max(scores.items(), key=lambda kv: kv[1])
        itype = best if hits > 0 else IncidentType.OTHER
        urgency = 5 if any(w in t for w in URGENT) else 3 if hits else 2
        conf = min(0.9, 0.5 + 0.15 * hits) if hits else 0.3
        return {"type": itype, "confidence": round(conf, 2), "urgency": urgency}
