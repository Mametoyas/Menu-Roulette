# Sprint 1 Plan: Recipe Roulette (Base Logic & Engine)

## Project Overview
- Topic: Recipe Roulette (Random recipe search by ingredients)
- Sprint Focus: Core modular functions, mock data engine, and input sanitization

## Roles & Responsibilities
- Planner (Jane): Architecture specification, DoD definition, PLAN.md
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


Sprint 3: GUI Development & Full-Stack IntegrationFocus & ObjectivesDevelop a Graphical User Interface (GUI) and integrate it with the Back-End engine developed in Sprints 1 and 2. Deliver a fully functional End-to-End application.  Architecture & Tech StackGUI Framework: Tkinter / CustomTkinterThreading: Background thread execution for API calls to prevent UI freezingPresentation Layer: Main Window, Search/Ingredient Input View, Recipe Display Card, Detail Modal, Favorites Manage