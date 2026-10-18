# Ain Al-Madina AI — Project Skeleton




---



## مصادر البيانات (Data Sources)

> قبل ما تعتمدي على أي داتاسيت: راجعي ترخيصه بنفسك، واذكريه في التقرير مع الورقة المرجعية.

### 1. صور الرؤية الحاسوبية (للـ Vision Agent)

#### الحفر وتلف الطرق: RDD2022
- **الاسم:** RDD2022 (Road Damage Dataset): 47,420 صورة من 6 دول (اليابان، الهند، التشيك، النرويج، أمريكا، الصين)، فيها أكتر من 55,000 تلف مُعلَّم.
- **الفئات:** شروخ طولية وعرضية وتمساحية، وحفر.
- **التحميل:** https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547
- **الورقة العلمية (للتقرير):** https://arxiv.org/abs/2209.08538 أو https://doi.org/10.1002/gdj3.260

[pothole](https://www.kaggle.com/datasets/andrewmvd/pothole-detection)



#### الحريق والدخان: D-Fire
- **الاسم:** D-Fire: أكتر من 21,000 صورة (21,527 حسب الأوراق)، بصيغة YOLO جاهزة، وفيها صور "ملخبطة" (غروب، ضباب) تقلل الإنذارات الكاذبة.
- **الموقع الرسمي للمؤلفين (GAIA):** https://github.com/gaiasd/DFireDataset
  (الرابط ده من المعرفة وما اتفتحش وقت البحث. لو ما اشتغلش جرّبي نسخة منقولة: https://github.com/sayedgamal99/DFireDataset)
- **نسخة على Roboflow:** https://universe.roboflow.com/uweeaai/d-fire-ehbj2

#### القمامة: TACO
- **الاسم:** TACO (Trash Annotations in Context): حوالي 1,500 صورة و4,784 تعليق (annotation) بصيغة COCO.
- **الموقع:** http://tacodataset.org
- **الكود:** https://github.com/pedropro/TACO
- **نسخة ثابتة على Zenodo:** https://zenodo.org/records/3354286
- **الورقة:** https://arxiv.org/abs/2003.06975

#### المياه والفيضان: FloodNet (استخدام محدود)
- **الاسم:** FloodNet: صور طائرات مسيّرة (UAV) بعد إعصار هارفي، فيها segmentation وVQA.
- **التحميل:** https://github.com/BinaLab/FloodNet-Supervised_v1.0
- **الورقة:** https://arxiv.org/abs/2012.02951
- **تنبيه:** الصور من فوق بالدرون، مش من كاميرا شارع، فمش مناسبة لكاميرات المجسم. ما اتلاقتش داتا مناسبة لتراكم مياه في الشارع، فالأفضل تصوري بنفسك على المجسم.

#### الحوادث المرورية

[Accident Detection From CCTV Footage (Kaggle)](https://www.kaggle.com/datasets/ckay16/accident-detection-from-cctv-footage)

[DoTA (Detection of Traffic Anomaly](https://github.com/MoonBlvd/Detection-of-Traffic-Anomaly)

[Roboflow Universe search {vehicle crash ,car accident}](https://universe.roboflow.com/)

### 2. الحساسات (للـ Sensor Agent)

- **Smoke Detection Dataset (IoT):** حوالي 60,000 قراءة (حرارة، رطوبة، ضغط، جسيمات، H2، Ethanol، CO2). الوصف: https://www.hackster.io/stefanblattmann/real-time-smoke-detection-with-ai-based-sensor-fusion-1086e6
  رابط Kaggle المباشر ما اتأكدش، فابحثي على Kaggle عن "Smoke Detection Dataset" باسم المؤلف Stefan Blattmann.
- **BME688/BME690 Smoke Dataset:** 131,370 عينة من حساسات غاز، لكن بحساسات Bosch مش MQ-2: https://data.mendeley.com/datasets/48j7mm8k56
- **تدفق المياه:** ما اتلاقتش داتا عامة مناسبة. سجّلي قراءات YF-S201 الطبيعية وغير الطبيعية بنفسك. وده أصلًا مطلوب للـ calibration وتحديد الـ thresholds (`HARD_THRESHOLD` و`NORMAL_MAX`).

[BattLeDIM](https://github.com/KIOS-Research/BattLeDIM)

[LeakDB](https://github.com/KIOS-Research/LeakDB)

[Numenta Anomaly](https://github.com/numenta/NAB)

[Smoke Detection Dataset](https://www.kaggle.com/datasets/deepcontractor/smoke-detection-dataset)

[UCI Gas Sensor Array Drift](https://archive.ics.uci.edu/dataset/224/gas+sensor+array+drift+dataset)


### 3. الخرائط (للـ Geo Agent)

- **OpenStreetMap عبر Geofabrik:** بتنزلي extract مصر (ملفات `.osm.pbf` أو shapefile)، ومنها تطلعي الطرق والمستشفيات والمدارس ومراكز الشرطة والإطفاء.
  - https://download.geofabrik.de (من صفحة Africa اختاري Egypt)
  - الترخيص **ODbL**، ولازم تذكري "© OpenStreetMap contributors" في التقرير.
  - لو محتاجة منطقة صغيرة بس (مدينتك أو الجامعة)، استخدمي Overpass API بدل تحميل مصر كلها.
  - بعد ما تطلعي المدارس والمستشفيات في ملف GeoJSON، حمّليها بـ `python -m backend.scripts.load_gis data/gis/places.geojson`.
- نسخة جاهزة بصيغة vector tiles: https://data.maptiler.com/downloads/dataset/osm/africa/egypt

### 4. اللي هتبنيه بنفسك

| المطلوب | الحل |
|---|---|
| صور المجسم الفعلي | تصوير بكاميرا Pi (تسرب، دخان، قمامة). أهم مصدر للـ fine-tuning |
| بلاغات المواطنين بالعامية المصرية | توليد بـ LLM + مراجعة يدوية لـ 50–100 مثال |
| لوائح الإدارات للـ RAG (اختياري) | وثائق رسمية عامة من الجهات نفسها |
| Ground truth للتقييم | 50–100 سيناريو معلَّم يدويًا في `data/eval/` |


  (Report Agent) (LLM or vision ) هنجمع الداتا 

[311 NYC](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9/about_data)

[Open311](https://www.open311.org/)



