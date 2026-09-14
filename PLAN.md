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