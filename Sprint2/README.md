# Sprint 2 - Back-End and API Integration

**Due: 25/09/2569 | Demo: 22-23/09/2569**

## Objective
- Live TheMealDB API, scoring/filter/rank, CI/CD, Kanban.

## Deliverables (commit b9ca681..5809544, 2026-09-19 to 2026-09-20)
- src/api_client.py - search_by_ingredient, get_meal_by_id, extract_ingredients, APIError
- src/recipe_engine.py - score_recipe, filter_and_rank, pick_random_recipe, format_recipe
- src/main.py - run_roulette_simulation CLI entry
- tests/test_api.py (10 tests, mocked HTTP)
- tests/test_engine.py (19 tests)
- tests/test_main.py (6 tests)
- .github/workflows/test.yml - pytest on push/PR to main/develop
- PLAN.md Sprint2 section, Sprint2.md QA report, img/Sprint2_TEST_report.png
- DESIGN.md GUI design basis

## Definition of Done
1. Live API fetch without DB layer
2. APIError handles timeout/bad response/empty results
3. CI passes pytest on PR to main/develop
4. Kanban updated with PR refs
5. PEP8 compliant

## Verify
- pytest tests/test_api.py tests/test_engine.py tests/test_main.py tests/test_sprint1.py -v
- 39 tests passed (10+19+6+4)

Full code lives in repo root src/ - this folder is the Sprint 2 submission pointer for 25/09/2569.
