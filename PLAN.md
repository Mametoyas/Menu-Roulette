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

## Sprint 3: GUI Development & Full-Stack Integration

### Focus & Objectives
Develop a **Graphical User Interface (GUI)** and integrate it with the Back-End engine from Sprints 1 & 2. Deliver a fully functional end-to-end application.

### Architecture & Tech Stack
| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| GUI Framework | `Tkinter` / `CustomTkinter` | Main UI rendering |
| Threading | `threading` (stdlib) | Non-blocking API calls |
| Presentation | Views & Modals | Search, Recipe Card, Detail, Favorites |

### Key Modules & File Structure
```text
src/
├── gui/
│   ├── app.py             # Main window & app entry point
│   ├── search_view.py     # Ingredient input & search bar
│   ├── recipe_card.py     # Recipe result card component
│   ├── detail_modal.py    # Full recipe detail popup
│   └── favorites_view.py  # Saved/favourites management screen
tests/
└── test_gui.py            # GUI integration & interaction tests
```

### Roles & Responsibilities
| Role | Member | Deliverable |
| :--- | :--- | :--- |
| Planner | Jane | Sprint plan, architecture diagram, DoD |
| Coder | Toey | `search_view.py`, input binding, threading |
| Coder | Ter | `recipe_card.py`, `detail_modal.py`, `favorites_view.py` |
| Debugger | Khong | GUI tests, QA report (`Sprint3.md`) |

### Definition of Done (DoD)
1. GUI launches without errors via `python -m src.main`.
2. Ingredient search triggers real API call and displays results as recipe cards.
3. Clicking a recipe card opens a detail modal with full information.
4. Favorites can be saved, viewed, and removed.
5. All API calls run on background threads — UI remains responsive at all times.
6. PEP 8 compliant code passing all `pytest` test cases.