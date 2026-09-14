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

### Focus & Objectives
Transition from Mock Data to real-time **TheMealDB API** integration and implement local **Data Persistence** using SQLite. Establish a robust Data Access Layer (DAL) and Business Logic Layer (BLL).

### Architecture & Tech Stack
- **HTTP Client**: `requests` package (Handling GET queries, parameters, JSON parsing, and HTTP status codes)
- **Persistence Layer**: SQLite (`recipes.db`) via standard library `sqlite3`
- **Testing**: `pytest` + `unittest.mock` / `requests-mock` for API testing without live network calls

### Key Modules & File Structure
```text
src/
├── api_client.py      # TheMealDB API requests & JSON parsing
├── db_manager.py      # SQLite connection, schema creation, CRUD operations
└── recipe_engine.py   # Business logic connecting API, Database, and Filtering
tests/
├── test_api.py        # Mock unit tests for API calls and error handling
└── test_db.py         # In-memory SQLite CRUD unit tests
```

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
4. Favorites can be saved, viewed, and removed persistently via SQLite.
5. All API calls run on background threads — UI remains responsive at all times.
6. PEP 8 compliant code passing all `pytest` test cases.