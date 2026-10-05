<a id="top"></a>

[README](../README.md) | [Members](../MEMBERS.md) | [Plan](../PLAN.md) | [Design](../DESIGN.md) | [Sprint1](../Sprint1/README.md) | [Sprint2](../Sprint2/README.md) | [Sprint3](../Sprint3/README.md) | [Sprint4](README.md) | [Changelog](../CHANGELOG.md) | [Review](../SPRINT_REVIEW.md) | [Peer Eval](../PEER_EVALUATION.md)

# Sprint 4 (Final Sprint) - Interactive Showcase & Feature Completion

**Final Presentation & Live Showcase Sprint**

## Objective
ยกระดับ Recipe Roulette สู่เวอร์ชันสมบูรณ์พร้อมนำเสนอ (Final Demo):
1. **Interactive Roulette Wheel**: วงล้อสุ่มหมุนจริง (Animated Canvas Wheel) พร้อม Easing Physics และเอฟเฟกต์เฉลิมฉลอง Confetti
2. **Favorites System**: แท็บเมนูโปรด (`#nav-favorites`) พร้อมระบบบันทึกสูตรอาหารลง LocalStorage
3. **Smart Shopping List**: แยกแยะวัตถุดิบที่มีและที่ยังขาด (Missing Ingredients) พร้อมปุ่มคัดลอกลง Clipboard
4. **Cuisine & Category Filter**: ตัวกรองประเภทและสัญชาติอาหารก่อนทำการค้นหาหรือสุ่ม

## Key Deliverables
- `static/js/app.js`: เพิ่มระบบ Canvas Roulette Wheel, LocalStorage Sync, และ Shopping List Clipboard API
- `static/css/style.css`: สไตล์วงล้อหมุน เข็มชี้ และ Modal สำหรับฉลองผลสุ่ม
- `templates/base.html`: เพิ่มแท็บนำทาง 2 แท็บ (`Explore`, `Favorites`) พร้อม Badges
- `templates/index.html` & `templates/_results_section.html`: แถบตัวกรอง Category/Cuisine และปุ่ม Favorite ❤️
- `src/recipe_engine.py`: ฟังก์ชันสนับสนุนการกรอง Category / Cuisine (Area)
- `tests/test_final_sprint.py`: Unit tests ครอบคลุมฟังก์ชันและการกรองใหม่ทั้งหมด

## Definition of Done (DoD)
1. เมื่อกดปุ่ม "Spin the Roulette" วงล้อกราฟิกจะปรากฏขึ้นพร้อมชื่อเมนู หมุนชะลอความเร็วอย่างสมจริง และยิง Confetti เมนูที่ได้รับ
2. แท็บ Navigation มีครบทั้ง Explore, Favorites และสลับหน้าได้อย่างลื่นไหล
3. หน้ารายละเอียดสูตรอาหารระบุวัตถุดิบที่ขาด พร้อมปุ่มคัดลอกรายการไปซื้อของ
4. ตัวกรอง Cuisine / Category ทำงานถูกต้องร่วมกับ Search และ Random Engine
5. โค้ดผ่านมาตรฐาน PEP 8 และ Unit Tests ใน `pytest` ผ่าน 100%

## Role-Based Assignment - Final Sprint
- **Planner (Khong)**: กำหนด Integration Spec, แผนสคริปต์ Demo 5 นาที, อัปเดตเอกสาร `PLAN.md` และ `README.md`
- **Coder 1 (Toey)**: พัฒนา Canvas Roulette Wheel, Animation Easing, Confetti Effect, และ Shopping List
- **Coder 2 (Benz)**: พัฒนา Navigation Tabs (Favorites), LocalStorage Engine, และ Cuisine Filter
- **Debugger (Ter)**: เขียน Unit Tests สำหรับ Engine/Web ใหม่, ตรวจสอบ Responsive ทุกขนาดหน้าจอ, จัดทำ Final QA Log

---

[Back to top](#top) | [README](../README.md)

## Progress - Part 1 done

- Wheel: canvas slices + easeOutCubic landing on winner + hand-rolled confetti + reduced-motion fallback (static/js/app.js, static/css/style.css)
- Tests: tests/test_final_sprint.py 4 tests (wheel payload contract, mocked)
- pytest: 53 passed
- Remaining: favorites tab (localStorage), shopping list, cuisine/category filter

## Progress - Parts 2-4 done

- Favorites: localStorage store, Favorites tab + badge, card hearts, modal save toggle (no login needed)
- Shopping: missing-ingredient marks + tag in modal, copy-to-clipboard with fallback
- Filter: category/area chips from live results, client-side, combinable, reset via All/Clear
- Verified: node --check OK, wheel landing math OK (n=3/7/10), pytest 53 passed

AI log ฉบับเต็มของ Sprint นี้: [LEARNINGLOG.md](LEARNINGLOG.md)

## Progress - CD done (repo side)

- Restored vercel.json (rewrites to /api/index) + api/index.py (Flask WSGI entry), verified GET / returns 200
- Remaining (dashboard): Import repo in Vercel + auto-deploy on push to main
