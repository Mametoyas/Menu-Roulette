<a id="top"></a>

[README](README.md) | [Members](MEMBERS.md) | [Plan](PLAN.md) | [Design](DESIGN.md) | [Sprint1](Sprint1/README.md) | [Sprint2](Sprint2/README.md) | [Sprint3](Sprint3/README.md) | [Changelog](CHANGELOG.md) | [Review](SPRINT_REVIEW.md) | [Peer Eval](PEER_EVALUATION.md)

# Sprint 1 Plan: Recipe Roulette (Base Logic & Engine)

## Project Overview
- Topic: Recipe Roulette (Random recipe search by ingredients)
- Sprint Focus: Core modular functions, mock data engine, and input sanitization

## Roles & Responsibilities
- Planner (Benz): Architecture specification, DoD definition, PLAN.md
- Coder (Toey): Text utilities, data cleaning, and input validation (`src/utils.py`)
- Coder (Ter): Mock recipe dataset and matching engine (`src/recipe_engine.py`)
- Debugger (Khong): Unit testing, edge-case validation, and QA report (`tests/test_sprint1.py`)

## Definition of Done (DoD)
1. Input string correctly trimmed, lowercased, and converted into clean lists.
2. Mock dataset contains at least 5 structured recipes matching TheMealDB schema.
3. Edge cases (empty input, numeric symbols, no matching recipe) handled with custom exceptions without throwing raw tracebacks.
4. PEP 8 compliant code passing all `pytest` test cases.

---

## Sprint 2: Back-End, API Integration & Data Persistence

## Project Overview
- **Topic**: Recipe Roulette (Random recipe search by ingredients)
- **Sprint Focus**: API Integration (TheMealDB), In-Memory Processing, CI/CD Pipeline, and Kanban Execution

### การแบ่งบทบาทหน้าที่ประจำ Sprint 2 (Rotation Roles)
- **เต้ย (Planner)**: รับผิดชอบการบริหารจัดการ Kanban Board, วางแผนและจัดสรร Task Backlog, อัปเดตเอกสาร PLAN.md และ README.md, กำหนดมาตรฐาน Git Branching Strategy และ Code Review Checklist
- **โขง (Coder)**: รับผิดชอบการพัฒนาโมดูล src/api_client.py เชื่อมต่อ TheMealDB API, ดึงข้อมูล JSON และจัดการ Error/HTTP Status Code ต่างๆ โดยใช้ environment variable (MEALDB_BASE_URL) ผ่าน os.getenv พร้อมค่า default
- **เบนซ์ (Coder)**: รับผิดชอบการพัฒนาโมดูล src/recipe_engine.py สำหรับประมวลผลข้อมูลวัตถุดิบ คำนวณ Match Score, Filtering และสุ่มเลือกเมนูแนะนำ (Random Recommendation)
- **เตอร์ (Debugger)**: รับผิดชอบการเขียน Unit Test แบบ Mocking API (tests/test_api.py, tests/test_engine.py), การตั้งค่า CI/CD Automation ผ่าน GitHub Actions (.github/workflows/test.yml) และจัดทำ QA Report

### โครงสร้างโค้ดใหม่สำหรับ Sprint 2 (Pure Code + API)
```text
    Menu-Roulette/
    ├── .github/
    │   └── workflows/
    │       └── test.yml          # CI/CD: Automated pytest workflow
    ├── src/
    │   ├── __init__.py
    │   ├── utils.py               # Input cleaning & validation (จาก Sprint 1)
    │   ├── api_client.py          # TheMealDB API requests & JSON extraction
    │   ├── recipe_engine.py       # Scoring, filtering & random selection
    │   └── main.py                # CLI Application entry point
    ├── tests/
    │   ├── test_utils.py          # Input validation tests
    │   ├── test_api.py            # API client tests using unittest.mock
    │   └── test_engine.py         # Business logic & recommendation engine tests
    ├── PLAN.md                    # Sprint planning & backlog details
    ├── README.md                  # Project overview & documentation
    └── requirements.txt
```
## Scoring Algorithm

Recipes retrieved from the API are ranked based on ingredient coverage using the following formula:

$$\text{Score} = \frac{\text{Matched User Ingredients}}{\text{Total User Ingredients}}$$

## Definition of Done (DoD)
1. Live execution fetches matching recipes from TheMealDB API without a database layer.
2. Custom exceptions handle API timeouts, bad responses, or empty search results gracefully.
3. Automated CI/CD pipeline passes all `pytest` unit tests on Pull Requests to `main`/`develop`.
4. Kanban board is completely updated with clear Pull Request references.
5. All codebase complies with PEP 8 standards.

---

## Technical Stack & Workflow
- **HTTP Client**: `requests`
- **Testing & Mocking**: `pytest`, `unittest.mock`
- **CI/CD**: GitHub Actions
- **Project Management**: GitHub Projects (Kanban Board)

## Key Deliverables & Branching Strategy
- `feature/api-client`: Developed by Khong (`src/api_client.py`)
- `feature/recipe-engine`: Developed by Benz (`src/recipe_engine.py`)
- `feature/cicd-testing`: Developed by Ter (`.github/workflows/test.yml`, `tests/`)
- `docs/sprint2-plan`: Managed by Toey (`PLAN.md`, `README.md`)


---

## Sprint 3: Web Application Development & Full-Stack Integration

### Focus & Objectives
Develop a **Web Application** using **Flask** and integrate it with the Back-End engine from Sprints 1 & 2. Deliver a fully functional end-to-end web app that runs in the browser. All business logic (validation, scoring, filtering, random pick) is reused directly from the pure back-end modules — the web layer is a thin presentation wrapper. UI follows the `DESIGN.md` design system (warm culinary style, Tailwind).

### Architecture & Tech Stack
| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| Web Framework | `Flask` | HTTP server, routing, request handling |
| Templating | Jinja2 (Flask) | Server-side HTML rendering |
| Frontend | HTML5 + CSS (Tailwind CDN) + JS (`fetch`) | Responsive UI, detail modal, roulette spin |
| State | In-Memory module store | Selected ingredients & favorites persistence |
| Testing | `pytest` + Flask test client | Route & full-flow integration tests |

### Web Endpoints (Route Map)
| Method | Route | Purpose |
| :--- | :--- | :--- |
| GET | `/` | Explore — hero, ingredient input, quick chips |
| POST | `/api/search` | JSON `{ingredients}` → back-end engine → JSON result (async `fetch`) |
| GET | `/recipe/<meal_id>` | Full recipe detail JSON (modal data) |


### Key Modules & File Structure
```text
src/
├── web_app.py          # Flask app, routes & app entry point
├── api_client.py       # TheMealDB API client (Sprint 2)
├── recipe_engine.py    # Scoring, filtering & random selection (Sprint 2)
├── main.py             # CLI entry point (Sprint 2)
└── utils.py            # Input cleaning & validation (Sprint 1)
templates/
├── base.html           # Shared layout: header nav, footer, modal container
├── index.html          # Explore — ingredient input, chips, search/roulette, loading bar
└── _results_section.html  # Shared results grid + empty state partial
static/
├── css/style.css       # Custom styles layered on top of Tailwind
└── js/app.js           # Client interactivity: fetch search, modal, loading, spin
tests/
└── test_web.py         # Flask route & end-to-end integration tests
```

### Roles & Responsibilities
| Role | Member | Deliverable |
| :--- | :--- | :--- |
| Planner | Toey | Sprint plan, architecture diagram, DoD, README update |
| Coder | Khong | `web_app.py` routes, search flow binding, back-end integration |
| Coder | Benz | `templates/` + `static/` UI: recipe cards, detail modal, favorites view |
| Debugger | Ter | `test_web.py` tests, CI workflow update, QA report (`Sprint3.md`) |

### Definition of Done (DoD)
1. Web app launches without errors via `python src/web_app.py` and opens at `http://127.0.0.1:5000`.
2. Ingredient search on the web page triggers a real TheMealDB API call and renders results as recipe cards.
3. Clicking a recipe card opens a detail modal with full information (ingredients, measurements, instructions).
4. Favorites can be saved, viewed, and removed from the web UI.
5. API calls run server-side in Flask routes; the page stays responsive via async `fetch` without full-page reloads.
6. PEP 8 compliant code passing all `pytest` unit test cases (including new `test_web.py`).

---

## Sprint 4 (Final Sprint): Interactive Roulette, Favorites, Smart Shopping List & Cuisine Filter

### Focus & Objectives
ยกระดับโปรเจกต์สู่เวอร์ชันสมบูรณ์สำหรับ **Final Presentation & Live Showcase**:
1. **Interactive Visual Roulette Wheel**: เปลี่ยนจากการสุ่มธรรมดาเป็นการหมุนวงล้อเสมือนจริง (Animated Wheel of Fortune) มีการชะลอความเร็ว (Friction easing) และยิงเอฟเฟกต์ Confetti เมื่อได้เมนูผู้ชนะ
2. **Favorites System & Dedicated Tab**: เพิ่มแท็บ Favorites (`#nav-favorites`) บน Navigation Bar พร้อม Badge สีแดง (`bg-rose-500`) ตามที่ระบุใน DESIGN.md ให้ผู้ใช้กด ❤️ เพื่อบันทึก/ดูสูตรที่ชอบได้ โดยเก็บใน `localStorage`
3. **Missing Ingredients & Smart Shopping List**: แสดงวัตถุดิบที่มีและที่ยังขาดอย่างชัดเจนใน Modal พร้อมปุ่ม **"Copy Shopping List"** สำหรับนำไปซื้อของต่อได้ทันที
4. **Cuisine & Category Filter Chips**: ตัวกรองประเภทอาหาร (Category) และสัญชาติ (Cuisine/Area) เพื่อความแม่นยำในการคัดเลือกเมนูก่อนสุ่ม

### Architecture & Tech Stack Additions
| Component | Technology | Purpose |
| :--- | :--- | :--- |
| Interactive Wheel | HTML5 Canvas / CSS Animation | จำลองวงล้อสุ่มหมุนจริงแบบมีฟิสิกส์การชะลอและเข็มชี้ |
| Celebration FX | Canvas-Confetti (Lightweight JS) | พลุกระดาษเฉลิมฉลองเมื่อวงล้อหยุดหมุนที่เมนูแนะนำ |
| Client Persistence | Web Storage API (`localStorage`) | จดจำสูตรอาหารโปรด (Favorites) ข้าม Session |
| Smart Shopping List | JavaScript String/DOM Builder + Clipboard API | คัดแยก Missing Ingredients และกดคัดลอกลง Clipboard |
| Automated Testing | `pytest` + Flask test client | ทดสอบ Endpoint และ Client/Server Contract สำหรับฟีเจอร์ใหม่ |

### Web Endpoints & Client State Map
| Method | Route / Storage | Purpose |
| :--- | :--- | :--- |
| GET | `/` | Explore — ค้นหาวัตถุดิบ, กรอง Cuisine/Category, และหมุนวงล้อ Roulette |
| POST | `/api/search` | ค้นหาและคำนวณ Match Score ตามวัตถุดิบ พร้อมรองรับ Category/Area filter |
| GET | `/recipe/<meal_id>` | ดึงข้อมูลสูตรฉบับเต็มเพื่อแสดงใน Modal และคำนวณ Missing Ingredients |
| Client | `localStorage['mr_favorites']` | จัดเก็บรายการเมนูโปรด (Array of recipe objects) |

### Key Modules & File Modifications
```text
Menu-Roulette/
├── templates/
│   ├── base.html             # เพิ่มแท็บนำทาง Favorites พร้อม Notification Badge
│   ├── index.html            # เพิ่มแถบตัวกรอง Cuisine/Category และโครงสร้าง Roulette Canvas
│   └── _results_section.html # เพิ่มปุ่มกด Favorite ❤️ และการแสดง Missing Badge
├── static/
│   ├── css/style.css         # สไตล์วงล้อ Roulette, Confetti, และ Modal ปรับแต่งพิเศษ
│   └── js/app.js             # Canvas Roulette Wheel, LocalStorage Sync, Shopping List Copy
├── src/
│   ├── recipe_engine.py      # ฟังก์ชันกรองเสริมตาม Category / Cuisine (Area)
│   └── web_app.py            # รองรับ Query Parameters เสริมสำหรับการกรอง
└── tests/
    └── test_final_sprint.py  # Unit tests สำหรับการกรอง Cuisine และ Edge Cases ใหม่
```

### Roles & Responsibilities (Agile Rotation)
| Role | Member | Deliverable |
| :--- | :--- | :--- |
| **Planner** | **Ter (เตอร์)** | ออกแบบ User Story สำหรับการนำเสนอ, วางสคริปต์ Demo Flow 5 นาที, อัปเดต `PLAN.md` และ `README.md` |
| **Coder 1 (Frontend)** | **Khong (โขง)** | พัฒนา Canvas Roulette Wheel Animation, Easing Physics, Confetti Effect, และ Shopping List Clipboard |
| **Coder 2 (Full-Stack)** | **Benz (เบ็นซ์)** | พัฒนาระบบ Favorites Tab, Favorites Manager (LocalStorage Sync), และตัวกรอง Category/Cuisine |
| **Debugger** | **Toey (เต้ย)** | เขียน Unit Tests สำหรับโมดูลใหม่, ตรวจสอบ Responsive Layout ทุกหน้าจอ, และจัดทำ QA Report สำหรับ Demo |

### Definition of Done (DoD) - Sprint 4
1. **Interactive Roulette Wheel**: เมื่อกด Spin the Roulette ระบบจะเปิด Modal วงล้อกราฟิกที่มีชื่อเมนูแบ่งเป็นช่อง หมุนชะลอความเร็วจนหยุดที่เมนูผู้ชนะ พร้อมแสดงเอฟเฟกต์ Confetti
2. **Navigation Tabs สมบูรณ์**: Navigation bar มีครบทั้งแท็บ `Explore` และ `Favorites` สลับหน้าไปมาได้อย่างลื่นไหลโดยไม่ต้อง Reload หน้า
3. **Favorites Persistence**: เพิ่ม/ลบ สูตรโปรดใน Favorites แล้ว เมื่อรีเฟรชหน้าเว็บหรือเปิดใหม่ ข้อมูลยังคงอยู่ครบถ้วน (`localStorage`)
4. **Smart Shopping List**: ในหน้ารายละเอียดสูตรอาหาร สามารถแยกแยะส่วนผสมที่มีและส่วนผสมที่ขาดได้ พร้อมมีปุ่มคลิกเดียวเพื่อคัดลอก Shopping List
5. **Cuisine & Category Filter**: สามารถเลือกกรองประเภทอาหาร (เช่น Seafood, Vegetarian) หรือสัญชาติอาหาร (เช่น Thai, Italian) ก่อนสุ่มได้
6. **Code Quality & Tests**: โค้ดผ่านมาตรฐาน PEP 8 และ Unit Tests ทั้งหมดใน `pytest` ผ่าน 100% (รวมชุดทดสอบใหม่)

---

[Back to top](#top) | [README](README.md)
