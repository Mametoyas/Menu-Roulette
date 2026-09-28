<a id="top"></a>

[README](README.md) | [Members](MEMBERS.md) | [Plan](PLAN.md) | [Design](DESIGN.md) | [Sprint1](Sprint1/README.md) | [Sprint2](Sprint2/README.md) | [Sprint3](Sprint3/README.md) | [Changelog](CHANGELOG.md) | [Review](SPRINT_REVIEW.md) | [Peer Eval](PEER_EVALUATION.md)

# Changelog - Menu Roulette

## Sprint 1 - Base Logic and Engine (14/09/2569 19:32 - 15/09/2569 09:48, due 18/09/2569)

Objective: Core modular functions, mock data engine, input sanitization.
Deliverables:
- src/utils.py - clean_ingredient_input, InvalidIngredientError
- src/recipe_engine.py - MOCK_RECIPES 5 recipes, filter_recipes_by_ingredients
- src/main.py - early CLI entry
- tests/test_sprint1.py
- PLAN.md Sprint1 section, Sprint1.md QA report, img/Sprint1_report.png

## Sprint 2 - Back-End and API Integration (19/09/2569 16:08 - 20/09/2569 21:55, due 25/09/2569)

Objective: Live TheMealDB API, scoring/filter/rank, CI/CD.
Deliverables:
- src/api_client.py - search_by_ingredient, get_meal_by_id, extract_ingredients
- src/recipe_engine.py - score_recipe, filter_and_rank, pick_random_recipe, format_recipe
- src/main.py - run_roulette_simulation CLI entry
- tests/test_api.py, tests/test_engine.py, tests/test_main.py
- .github/workflows/test.yml
- PLAN.md Sprint2 section, Sprint2.md QA report, img/Sprint2_TEST_report.png
- DESIGN.md GUI design basis
Tests: 39 passed (10+19+6+4)

## Sprint 3 - Web App Full-Stack (20/09/2569 22:05 - 20/09/2569 23:57, due 02/10/2569)

Objective: Flask web app reusing Sprint 1+2 engine, async fetch, modal, roulette.
Deliverables:
- src/web_app.py - GET /, POST /api/search, GET /recipe/<id>
- src/app.py - Vercel entry
- templates/base.html, templates/index.html, templates/_results_section.html
- static/css/style.css, static/js/app.js
- tests/test_web.py
- PLAN.md Sprint3 section, README Sprint3 section

Note: Sprint1/ Sprint2/ Sprint3/ folders are submission pointers - real code stays in src//templates//static//tests/.

---

[Back to top](#top) | [README](README.md)
