# Sprint Review and Retrospective

Project: Menu Roulette (Recipe Roulette)
Stack: Python 3.11, Flask 3, requests, pytest, TheMealDB API
Pointers: Sprint1/README.md, Sprint2/README.md, Sprint3/README.md, CHANGELOG.md

## 1. Sprint 1 Review - Base Logic and Engine (14/09/2569 19:32 - 15/09/2569 09:48, due 18/09/2569)

Scope: utils.clean_ingredient_input, recipe_engine MOCK_RECIPES, tests/test_sprint1.py
Result: 7 tests passed. Input trim/lower/dedup works. Mock filter works offline.

### QA Test Log - Sprint 1

| ID | Input | Expected | Actual | Status |
|---|---|---|---|---|
| TC-S1-01 | Pork , Egg! , garlic | [pork, egg, garlic] | normalized list | PASSED |
| TC-S1-02 | pork, egg123 | InvalidIngredientError | raised numbers error | PASSED |
| TC-S1-03 | blank / whitespace only | InvalidIngredientError | raised empty error | PASSED |
| TC-S1-04 | [pork] filter | 2 recipes with pork | 2 matches | PASSED |
| TC-S1-05 | [avocado] filter | 0 matches, pick None | [] and None | PASSED |

### Retrospective - Sprint 1

Wow: Engine decoupled from UI, pytest mocking fast and reliable.
Whoops: Regex stripped inner spaces (soy sauce -> soysauce). Fixed in utils.py to keep spaces.

## 2. Sprint 2 Review - Back-End and API (19/09/2569 16:08 - 20/09/2569 21:55, due 25/09/2569)

Scope: src/api_client.py, src/recipe_engine.py scoring/rank, src/main.py, CI test.yml
Result: 39 tests passed (test_api 10 + test_engine 19 + test_main 6 + test_sprint1 4). No live network in tests (unittest.mock).

### QA Test Log - Sprint 2

| ID | Input | Expected | Actual | Status |
|---|---|---|---|---|
| TC-S2-01 | search_by_ingredient(chicken) 200 | 2 meals 52772,52968 | 2 returned | PASSED |
| TC-S2-02 | search avocado meals:null | [] | [] | PASSED |
| TC-S2-03 | search status 500 | APIError | raised | PASSED |
| TC-S2-04 | search Timeout | APIError | raised | PASSED |
| TC-S2-05 | get_meal_by_id(52772) | Teriyaki Chicken dict | valid dict | PASSED |
| TC-S2-06 | get_meal_by_id(99999) null | None | None | PASSED |
| TC-S2-07 | get_meal 500 / Timeout | APIError | raised | PASSED |
| TC-S2-08 | extract_ingredients | [chicken, soy sauce, garlic] | 3 items, no empty | PASSED |
| TC-S2-09 | search_recipes [chicken,pork] overlap | 2 unique, 2 detail calls | dedup OK | PASSED |
| TC-S2-10 | search_recipes [] | [] no API call | not called | PASSED |
| TC-S2-11 | search missing details None | [] skipped | [] | PASSED |
| TC-S2-12 | score [chicken,rice] full | 1.0 | 1.0 | PASSED |
| TC-S2-13 | score [chicken,pork] partial | 0.5 | 0.5 | PASSED |
| TC-S2-14 | score [avocado] / [] | 0.0 no div-zero | 0.0 | PASSED |
| TC-S2-15 | filter_and_rank sort desc | sorted high-low | sorted | PASSED |
| TC-S2-16 | min_score 1.0 none qualify | [] | [] | PASSED |
| TC-S2-17 | no mutate input dicts | no score key | clean | PASSED |
| TC-S2-18 | pick top score 1.0x2 + 0.5 | pick 1.0 only | top only | PASSED |
| TC-S2-19 | pick [] / legacy no-score | None / random one | OK | PASSED |
| TC-S2-20 | format_recipe full/missing | friendly keys, defaults | mapped | PASSED |
| TC-S2-21 | run_roulette Pork,Garlic | success formatted selected+top | GUI-ready | PASSED |
| TC-S2-22 | run_roulette avocado,tofu | 0 matches selected None | empty OK | PASSED |
| TC-S2-23 | run_roulette API fail / numbers / empty | error status | error dict | PASSED |

### Retrospective - Sprint 2

Wow: Full HTTP mocking makes API tests deterministic, no flaky network. CI runs pytest -v on push/PR.
Whoops: Mock dicts used ingredients key but live API uses strIngredient1..20. Added _recipe_ingredients normalizer and tests.

## 3. Sprint 3 Review - Web Full-Stack (20/09/2569 22:05 - 20/09/2569 23:57, due 02/10/2569)

Scope: src/web_app.py, templates/, static/, tests/test_web.py
Result: 6 web tests passed. Routes: GET /, POST /api/search, GET /recipe/<id>.

### QA Test Log - Sprint 3

| ID | Input | Expected | Actual | Status |
|---|---|---|---|---|
| TC-S3-01 | GET / | 200 contains fridge | rendered | PASSED |
| TC-S3-02 | POST /api/search pork,garlic | success 1 top Pork Souvlaki | JSON OK | PASSED |
| TC-S3-03 | POST invalid pork 123 | error status | error JSON | PASSED |
| TC-S3-04 | POST API fail | error message | error JSON | PASSED |
| TC-S3-05 | GET /recipe/52968 | Pork Souvlaki Greek | formatted JSON | PASSED |
| TC-S3-06 | GET /recipe/99999 | 404 Recipe not found | 404 JSON | PASSED |

### Retrospective - Sprint 3

Wow: Thin web layer reuses Sprint 1+2 engine unchanged. Async fetch keeps page responsive. Modal + roulette + loading bar per DESIGN.md.
Whoops: Template/static path broke under pytest vs python src/web_app.py. Fixed with PROJECT_ROOT anchor. Vercel entry needed src/app.py re-export.

## 4. Overall DoD Check

- [x] Modular layers: presentation / business logic / data access separated
- [x] Search / filter / sort-score / rank / random pick working
- [x] Input validation + APIError handling, no raw traceback to user
- [x] pytest suite green (sprint1 7 + sprint2 39 + sprint3 6, overlap counted once)
- [x] CI workflow .github/workflows/test.yml

