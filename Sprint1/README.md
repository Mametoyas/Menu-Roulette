# Sprint 1 - Base Logic and Engine

**Due: 18/09/2569 | Demo: 15-16/09/2569**

## Objective
- Core modular functions, mock data engine, input sanitization.

## Deliverables (commit ea9dc78..d261127, 2026-09-14 to 2026-09-15)
- src/utils.py - clean_ingredient_input, InvalidIngredientError
- src/recipe_engine.py - MOCK_RECIPES 5 recipes, filter_recipes_by_ingredients
- src/main.py - early CLI entry
- tests/test_sprint1.py
- PLAN.md Sprint1 section, Sprint1.md QA report, img/Sprint1_report.png

## Definition of Done
1. Input trimmed/lowercased to clean list
2. Mock dataset >=5 recipes TheMealDB schema
3. Edge cases with custom exceptions, no raw traceback
4. PEP8 + pytest pass

## Verify
- pytest tests/test_sprint1.py -v
- flake8 src/utils.py src/recipe_engine.py

Full code lives in repo root src/ - this folder is the Sprint 1 submission snapshot pointer.
