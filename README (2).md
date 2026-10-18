# web/ — React + Vite + Tailwind (Responsive PWA)

لسه فاضي عمدًا. الترتيب المقترح بعد ما الـ API يشتغل:
1. `npm create vite@latest . -- --template react-ts`
2. صفحات: `/command` (خريطة Leaflet + قائمة حوادث + تفاصيل)، `/department` (حوادثي + تم الحل)، `/report` (كاميرا + GPS).
3. الاتصال بـ `POST /auth/login` ثم `GET /incidents` و`WS /ws/incidents?token=...`.
