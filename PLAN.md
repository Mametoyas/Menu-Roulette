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
- **โขง (Coder)**: รับผิดชอบการพัฒนาโมดูล src/api_client.py เชื่อมต่อ TheMealDB API, ดึงข้อมูล JSON และจัดการ Error/HTTP Status Code ต่างๆ โดยใช้ .env ด้วยในการจัดการ environment variables
- **เบ็นซ์ (Coder)**: รับผิดชอบการพัฒนาโมดูล src/recipe_engine.py สำหรับประมวลผลข้อมูลวัตถุดิบ คำนวณ Match Score, Filtering และสุ่มเลือกเมนูแนะนำ (Random Recommendation)
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
| Planner | Jane | Sprint plan, architecture diagram, DoD, README update |
| Coder | Toey | `web_app.py` routes, search flow binding, back-end integration |
| Coder | Ter | `templates/` + `static/` UI: recipe cards, detail modal, favorites view |
| Debugger | Khong | `test_web.py` tests, CI workflow update, QA report (`Sprint3.md`) |

### Definition of Done (DoD)
1. Web app launches without errors via `python src/web_app.py` and opens at `http://127.0.0.1:5000`.
2. Ingredient search on the web page triggers a real TheMealDB API call and renders results as recipe cards.
3. Clicking a recipe card opens a detail modal with full information (ingredients, measurements, instructions).
4. Favorites can be saved, viewed, and removed from the web UI.
5. API calls run server-side in Flask routes; the page stays responsive via async `fetch` without full-page reloads.
6. PEP 8 compliant code passing all `pytest` unit test cases (including new `test_web.py`).