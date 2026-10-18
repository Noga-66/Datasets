







# Ain Al-Madina AI — مصادر البيانات (Data Sources)


---

## 1. صور الرؤية الحاسوبية (Vision Agent)

| الفئة | الداتاسيت | الوصف | الروابط |
|---|---|---|---|
| الحفر وتلف الطرق | **RDD2022** | 47,420 صورة من 6 دول (اليابان، الهند، التشيك، النرويج، أمريكا، الصين)، فيها أكتر من 55,000 تلف معلَّم. الفئات: شروخ طولية وعرضية وتمساحية، وحفر | [التحميل (Figshare)](https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547) · [الورقة (arXiv)](https://arxiv.org/abs/2209.08538) · [الورقة (DOI)](https://doi.org/10.1002/gdj3.260) |
| الحفر | **Pothole Detection** | داتاسيت حفر على Kaggle | [Kaggle](https://www.kaggle.com/datasets/andrewmvd/pothole-detection) |
| الحريق والدخان | **D-Fire** | أكتر من 21,000 صورة (21,527 حسب الأوراق) بصيغة YOLO جاهزة، وفيها صور "ملخبطة" (غروب، ضباب) تقلل الإنذارات الكاذبة | [GAIA الرسمي](https://github.com/gaiasd/DFireDataset) · [نسخة منقولة](https://github.com/sayedgamal99/DFireDataset) · [Roboflow](https://universe.roboflow.com/uweeaai/d-fire-ehbj2) |
| القمامة | **TACO** (Trash Annotations in Context) | حوالي 1,500 صورة و4,784 annotation بصيغة COCO | [الموقع](http://tacodataset.org) · [الكود](https://github.com/pedropro/TACO) · [Zenodo](https://zenodo.org/records/3354286) · [الورقة](https://arxiv.org/abs/2003.06975) |
| المياه والفيضان (استخدام محدود) | **FloodNet** | صور طائرات مسيّرة (UAV) بعد إعصار هارفي، فيها segmentation وVQA | [التحميل](https://github.com/BinaLab/FloodNet-Supervised_v1.0) · [الورقة](https://arxiv.org/abs/2012.02951) |
| الحوادث المرورية | **Accident Detection From CCTV Footage** | فيديو كاميرات مراقبة | [Kaggle](https://www.kaggle.com/datasets/ckay16/accident-detection-from-cctv-footage) |
| الحوادث المرورية | **DoTA** (Detection of Traffic Anomaly) | كشف الشذوذ المروري | [GitHub](https://github.com/MoonBlvd/Detection-of-Traffic-Anomaly) |
| الحوادث المرورية | **Roboflow Universe** | ابحثي عن: `vehicle crash`, `car accident` | [Roboflow](https://universe.roboflow.com/) |

> **D-Fire:** رابط GAIA من المعرفة وما اتفتحش وقت البحث. لو ما اشتغلش، جرّبي النسخة المنقولة.

---

## 2. الحساسات (Sensor Agent)

| النوع | الداتاسيت | الوصف | الرابط |
|---|---|---|---|
| دخان | **Smoke Detection Dataset (IoT)** | حوالي 60,000 قراءة (حرارة، رطوبة، ضغط، جسيمات، H2، Ethanol، CO2) | [الوصف (Hackster)](https://www.hackster.io/stefanblattmann/real-time-smoke-detection-with-ai-based-sensor-fusion-1086e6) · [Kaggle](https://www.kaggle.com/datasets/deepcontractor/smoke-detection-dataset) |
| دخان / غاز | **BME688/BME690 Smoke Dataset** | 131,370 عينة من حساسات غاز، لكن بحساسات Bosch مش MQ-2 | [Mendeley](https://data.mendeley.com/datasets/48j7mm8k56) |
| غاز | **UCI Gas Sensor Array Drift** | قراءات حساسات غاز على مدى زمن طويل | [UCI](https://archive.ics.uci.edu/dataset/224/gas+sensor+array+drift+dataset) |
| تسرب المياه | **BattLeDIM** | بيانات شبكة مياه بتسريبات | [GitHub](https://github.com/KIOS-Research/BattLeDIM) |
| تسرب المياه | **LeakDB** | بيانات تسريبات مولَّدة بالمحاكاة | [GitHub](https://github.com/KIOS-Research/LeakDB) |
| كشف الشذوذ | **Numenta Anomaly Benchmark** | سلاسل زمنية فيها شذوذ | [GitHub](https://github.com/numenta/NAB) |
| تدفق المياه | — | ما اتلاقتش داتا عامة مناسبة | سجّلي قراءات YF-S201 الطبيعية وغير الطبيعية بنفسك |


---

## 3. الخرائط (Geo Agent)

| المصدر | الاستخدام | الرابط |
|---|---|---|
| **OpenStreetMap عبر Geofabrik** | تنزيل extract مصر (`.osm.pbf` أو shapefile)، ومنه تطلعي الطرق والمستشفيات والمدارس ومراكز الشرطة والإطفاء | [Geofabrik](https://download.geofabrik.de) (من صفحة Africa اختاري Egypt) |
| **Overpass API** | لو محتاجة منطقة صغيرة بس (مدينتك أو الجامعة) بدل تحميل مصر كلها | [Overpass Turbo](https://overpass-turbo.eu) |
| **MapTiler** | نسخة جاهزة بصيغة vector tiles | [MapTiler Egypt](https://data.maptiler.com/downloads/dataset/osm/africa/egypt) |


```

---

## 4. بلاغات المواطنين (Report Agent)

| المصدر | الاستخدام | الرابط |
|---|---|---|
| **311 NYC** | بلاغات حقيقية لاستخدام هيكل البلاغ وتصنيف الفئات | [NYC Open Data](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9/about_data) |
| **Open311** | معيار مفتوح لهيكل بلاغات المدن | [open311.org](https://www.open311.org/) |

---

## 5. اللي هتبنيه بنفسك

| المطلوب | الحل |
|---|---|
| صور المجسم الفعلي | تصوير بكاميرا Pi (تسرب، دخان، قمامة). أهم مصدر للـ fine-tuning |
| بلاغات المواطنين بالعامية المصرية | توليد بـ LLM + مراجعة يدوية لـ 50–100 مثال |
| لوائح الإدارات للـ RAG (اختياري) | وثائق رسمية عامة من الجهات نفسها |
| Ground truth للتقييم | 50–100 سيناريو معلَّم يدويًا في `data/eval/` |

[Open311](https://www.open311.org/)



