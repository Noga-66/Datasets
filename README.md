# Ain Al-Madina AI — Project Skeleton

هيكل مشروع شغّال (backend + infra + agents + simulation). **الواجهة (web) ولسه فاضية**، وده عمدًا.

## حالة الملفات (بصراحة)
| الجزء | الحالة |
|---|---|
| Agents (Sensor, Geo, Fusion, Priority, Routing, Report, Verification) | مكتوبة. الـ logic النقي **اتعمله unit tests ونجحت (7 tests)** |
| Vision Agent | مكتوب، لكن محتاج `ultralytics` وموديل متدرّب (`best.pt`) |
| Report Agent | keyword-based (baseline). استبداله بـ LLM = تحسين لاحق |
| Verification Agent | فحص الحساس شغال، فحص الصورة `TODO` (SSIM / إعادة YOLO) |
| Workers + API + docker-compose | مكتوبة، **لسه ما اتجرّبتش على Docker** (متوقع تحتاجي تظبطي حاجات صغيرة في أول تشغيل) |
| web/ + evaluation/replay.py + RAG | **لسه ما اتكتبوش** |

## التشغيل (أول مرة)
```bash
cp .env.example .env                      # غيّري الباسوردات وJWT_SECRET
bash infra/mosquitto/make_passwd.sh       # يوزرات MQTT (bridge, esp32_*, simulator)
docker compose up -d postgres kafka mosquitto minio
docker compose ps                         # استني healthy
bash infra/kafka/create_topics.sh
bash infra/minio/init_buckets.sh
docker compose run --rm api python -m backend.scripts.init_db
docker compose run --rm -e SEED_PASSWORD='غيّريه' api python -m backend.scripts.seed
docker compose run --rm api python -m backend.scripts.load_gis data/gis/places.geojson   # بعد تحميل بيانات OSM
docker compose up -d                      # باقي الخدمات (api + workers)
```
- Swagger: http://localhost:8000/docs  |  MinIO: http://localhost:9001  |  Kafka UI: `docker compose --profile debug up -d kafka-ui` ثم http://localhost:8080

## Smoke test (بدون هاردوير)
```bash
pip install -r simulation/requirements.txt
python simulation/scenario_runner.py --scenario water_leak
```
بعدها `POST /auth/login` كـ `operator1` ثم `GET /incidents`: لازم تلاقي حادث واحد فيه مصدرين (sensor + report).
لو ما ظهرش: اتبعي الرسالة في Kafka UI (`sensor.readings` → `events.perceived` → `incidents.updates`)، والمكان اللي وقفت فيه هو المشكلة.

## تشغيل الاختبارات
```bash
pip install pydantic pydantic-settings sqlalchemy pytest
PYTHONPATH=. pytest tests -q
```

## قرارات مهمة
- **حالات الحادث** = حالات البروبوزال: `DETECTED → ANALYZED → FUSED → PRIORITIZED → ASSIGNED → RESOLVED → VERIFIED` (+ `REOPENED`).
- `pipeline_worker` **نسخة واحدة** (علشان الـ Fusion ما يعملش حادثين لنفس المشكلة).
- كل threshold في `HARD_THRESHOLD` و`NORMAL_MAX` و`.env` هو **افتراض** لازم يتظبط بعد calibration الحساسات.
- إحداثيات `scripts/seed.py` مؤقتة: غيّريها لموقع المجسم. ولأن المجسم صغير، اضبطي `FUSION_RADIUS_M`.
- Kafka بـ broker واحد = prototype فقط.
