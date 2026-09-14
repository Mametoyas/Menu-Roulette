# Sprint 1 Plan: Recipe Roulette (Base Logic & Engine)

## Project Overview
- Topic: Recipe Roulette (Random recipe search by ingredients)
- Sprint Focus: Core modular functions, mock data engine, and input sanitization[cite: 3]

## Roles & Responsibilities[cite: 3]
- Planner (Jane): Architecture specification, DoD definition, PLAN.md[cite: 3]
- Coder (Toey): Text utilities, data cleaning, and input validation (`src/utils.py`)[cite: 3]
- Coder (Ter): Mock recipe dataset and matching engine (`src/recipe_engine.py`)[cite: 3]
- Debugger (Khong): Unit testing, edge-case validation, and QA report (`tests/test_sprint1.py`)[cite: 3]

## Definition of Done (DoD)[cite: 3]
1. Input string correctly trimmed, lowercased, and converted into clean lists[cite: 3].
2. Mock dataset contains at least 5 structured recipes matching TheMealDB schema[cite: 1, 3].
3. Edge cases (empty input, numeric symbols, no matching recipe) handled with custom exceptions without throwing raw tracebacks[cite: 3].
4. PEP 8 compliant code passing all `pytest` test cases[cite: 2, 3].