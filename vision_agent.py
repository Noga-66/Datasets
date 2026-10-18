"""Vision Agent: YOLO (ultralytics) محمّل مرة واحدة. الموديل لازم يتدرّب على الفئات المطلوبة."""
import io
from backend.agents.base import BaseAgent
from backend.config import settings
from backend.contracts.events import IncidentType

# اسم الكلاس في الموديل -> نوع الحادث (عدّليها حسب dataset.yaml بتاعك)
CLASS_MAP = {
    "pothole": IncidentType.POTHOLE, "D40": IncidentType.POTHOLE,
    "fire": IncidentType.FIRE_SMOKE, "smoke": IncidentType.FIRE_SMOKE,
    "garbage": IncidentType.GARBAGE, "trash": IncidentType.GARBAGE,
    "water": IncidentType.WATER_LEAK, "flood": IncidentType.WATER_LEAK,
}


class VisionAgent(BaseAgent):
    name = "vision"

    def __init__(self) -> None:
        super().__init__()
        self._model = None

    def _load(self):
        if self._model is None:
            from ultralytics import YOLO  # import متأخر: مكتبة ثقيلة
            self._model = YOLO(settings.vision_weights)
        return self._model

    def run(self, image_bytes: bytes) -> list[dict]:
        from PIL import Image
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        res = self._load().predict(img, conf=settings.vision_min_conf, verbose=False)[0]
        out = []
        for b in res.boxes:
            name = res.names[int(b.cls)]
            if name in CLASS_MAP:
                out.append({"type": CLASS_MAP[name], "confidence": round(float(b.conf), 2),
                            "bbox": [round(v, 1) for v in b.xyxy[0].tolist()]})
        return out
