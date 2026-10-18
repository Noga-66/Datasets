1. صور الرؤية الحاسوبية (للـ Vision Agent)

الحفر وتلف الطرق: RDD2022

اسمه: RDD2022 (Road Damage Dataset)، 47,420 صورة من 6 دول (اليابان، الهند، التشيك، النرويج، أمريكا، الصين)، فيها أكتر من 55,000 تلف مُعلَّم.
الفئات: شروخ طولية وعرضية وتمساحية، وحفر.
التحميل: https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547
الورقة العلمية (للتقرير): https://arxiv.org/abs/2209.08538 أو https://doi.org/10.1002/gdj3.260
ملاحظة: مصر مش من الدول دي، فشوارعنا مختلفة عنها. صوّري كمان صور محلية.

الحريق والدخان: D-Fire

اسمه: D-Fire، أكتر من 21,000 صورة (21,527 حسب الأوراق)، بصيغة YOLO جاهزة، وفيها صور "ملخبطة" (غروب، ضباب) تقلل الإنذارات الكاذبة.
الموقع الرسمي للمؤلفين (GAIA): https://github.com/gaiasd/DFireDataset (ده من معرفتي، ما فتحتوش في البحث، وطلعلي بس نسختين منقولتين، فلو ما اشتغلش جرّبي https://github.com/sayedgamal99/DFireDataset)
نسخة على Roboflow: https://universe.roboflow.com/uweeaai/d-fire-ehbj2

القمامة: TACO

اسمه: TACO (Trash Annotations in Context)، حوالي 1,500 صورة و4,784 تعليق (annotation) بصيغة COCO.
الموقع: http://tacodataset.org
الكود: https://github.com/pedropro/TACO
نسخة ثابتة على Zenodo: https://zenodo.org/records/3354286
الورقة: https://arxiv.org/abs/2003.06975
تنبيه: TACO بيصوّر مخلفات متفرقة (litter)، مش حاويات طافحة. لـ "تراكم القمامة" الأقرب في Roboflow Universe، ابحثي هناك عن “garbage overflow” أو “waste pile”. أنا ما لقيتش داتا بعينها أأكدلك عليها، وأغلب الظن هتحتاجي تضيفي صور من عندك.

المياه والفيضان: FloodNet (استخدام محدود)

اسمه: FloodNet، صور طائرات مسيّرة (UAV) بعد إعصار هارفي، فيها segmentation وVQA.
التحميل: https://github.com/BinaLab/FloodNet-Supervised_v1.0
الورقة: https://arxiv.org/abs/2012.02951
تنبيه: الصور من فوق بالدرون، مش من كاميرا شارع، فمش مناسبة لكاميرات المجسم. ما لقيتش داتا مناسبة لتراكم مياه في الشارع، فالأفضل تصوري بنفسك على المجسم.

الحوادث المرورية (اختياري)

اسمه: CADP (Car Accident Detection and Prediction)، 1,416 مقطع فيديو من YouTube، منها 205 بتعليق كامل: https://www.v7labs.com/open-datasets/cadp
بما إنها فيديوهات من YouTube، راجعي شروط الاستخدام قبل ما تعتمدي عليها.
2. الحساسات (للـ Sensor Agent)
Smoke Detection Dataset (IoT): حوالي 60,000 قراءة (حرارة، رطوبة، ضغط، جسيمات، H2، Ethanol، CO2). وصفها منشور هنا: https://www.hackster.io/stefanblattmann/real-time-smoke-detection-with-ai-based-sensor-fusion-1086e6. ما أكدتش رابط Kaggle المباشر، فابحثي على Kaggle عن “Smoke Detection Dataset” باسم المؤلف Stefan Blattmann.
BME688/BME690 Smoke Dataset: 131,370 عينة من حساسات غاز، لكن بحساسات Bosch مش MQ-2: https://data.mendeley.com/datasets/48j7mm8k56
تدفق المياه: ما لقيتش داتا عامة مناسبة، وأنصحك تسجلي قراءات YF-S201 الطبيعية وغير الطبيعية بنفسك. وده أصلًا مطلوب للـ calibration وتحديد الـ thresholds.
3. الخرائط (للـ Geo Agent)
OpenStreetMap عبر Geofabrik: بتنزلي extract مصر (ملفات .osm.pbf أو shapefile)، ومنها تطلعي الطرق والمستشفيات والمدارس ومراكز الشرطة والإطفاء.
https://download.geofabrik.de (من صفحة Africa اختاري Egypt)
الترخيص ODbL، ولازم تذكري “© OpenStreetMap contributors” في التقرير.
لو محتاجة منطقة صغيرة بس (مدينتك أو الجامعة)، استخدمي Overpass API بدل تحميل مصر كلها.
فيه كمان نسخة جاهزة بصيغة vector tiles: https://data.maptiler.com/downloads/dataset/osm/africa/egypt
