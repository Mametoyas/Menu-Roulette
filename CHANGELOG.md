<a id="top"></a>

[README](README.md) | [Members](MEMBERS.md) | [Plan](PLAN.md) | [Design](DESIGN.md) | [Sprint1](Sprint1/README.md) | [Sprint2](Sprint2/README.md) | [Sprint3](Sprint3/README.md) | [Changelog](CHANGELOG.md) | [Review](SPRINT_REVIEW.md) | [Peer Eval](PEER_EVALUATION.md)

# Changelog - Menu Roulette

Submission focus: Sprint 2 due 25/09/2569.

## Unreleased - Sprint 4 part 1

### Added

- Canvas roulette wheel landing on selected_recipe + hand-rolled confetti (static/js/app.js, static/css/style.css)
- tests/test_final_sprint.py (4 wheel payload contract tests, mocked)
\- Favorites tab + localStorage hearts/badge, missing-ingredient shopping list + copy, client-side category/area filter chips
- Vercel CD entry restored (vercel.json rewrites + api/index.py Flask function, GET / returns 200 verified)

### Files

```text
static/js/app.js         <- wheel + favorites + shopping + filter
static/css/style.css       <- wheel/confetti + fav/badge/missing/shopping styles
templates/base.html        <- Explore/Favorites tabs + fav badge
tests/test_final_sprint.py  <- 4 tests
vercel.json + api/index.py  <- Vercel CD entry
Sprint4/LEARNINGLOG.md     <- AI usage log
```

## [v0.1.0] - Sprint 1: Base Logic and Engine (14/09/2569 19:32 - 15/09/2569 09:48, due 18/09/2569)

### Added

- Initialized project structure with src/, tests/, img/
- Input cleaning and validation (clean_ingredient_input, InvalidIngredientError)
- Mock recipe dataset with 5 TheMealDB-schema recipes + ingredient filter
- Early CLI entry point
- Sprint 1 unit tests (tests/test_sprint1.py)
- PLAN.md Sprint 1 section + Sprint1.md QA report

### Files

```text
src/
├── utils.py            <- Input cleaning + validation
├── recipe_engine.py    <- MOCK_RECIPES + filter_recipes_by_ingredients
└── main.py             <- Early CLI entry

tests/
└── test_sprint1.py     <- Input + filter unit tests

PLAN.md                <- Sprint 1 plan + DoD
Sprint1.md             <- QA report
pytest.ini             <- pytest config (pythonpath = .)
requirements.txt       <- pytest + flake8 + black
```

## [v0.2.0] - Sprint 2: Back-End and API Integration (19/09/2569 16:08 - 20/09/2569 21:55, due 25/09/2569)

### Added

- Live TheMealDB API client (search_by_ingredient, get_meal_by_id, extract_ingredients, APIError)
- Match scoring, filter_and_rank, top-score random pick, GUI-friendly format_recipe
- CLI pipeline run_roulette_simulation (clean -> search/score/rank -> format -> pick)
- Mocked API/engine/main tests (39 tests, no live network)
- CI workflow: pytest on push/PR to main/develop
- PLAN.md Sprint 2 section + Sprint2.md QA report + DESIGN.md basis

### Files

```text
src/
├── api_client.py       <- TheMealDB requests + JSON parse + error handling
├── recipe_engine.py    <- score/filter/rank/pick/format
└── main.py             <- run_roulette_simulation + console

tests/
├── test_api.py         <- API client tests, mocked HTTP (10 tests)
├── test_engine.py      <- scoring/rank/pick/format tests (19 tests)
└── test_main.py        <- entry pipeline tests (6 tests)

.github/workflows/
└── test.yml            <- CI: pytest -v on Ubuntu Python 3.11

PLAN.md                <- Sprint 2 plan + DoD
Sprint2.md             <- QA report
DESIGN.md              <- GUI design basis
```

## [v0.3.0] - Sprint 3: Web App Full-Stack (20/09/2569 22:05 - 20/09/2569 23:57, due 02/10/2569)

### Added

- Flask web app reusing Sprint 1+2 engine (thin presentation layer)
- Routes: GET / explore page, POST /api/search JSON, GET /recipe/<id> detail
- Templates + static UI: cards, detail modal, loading bar, roulette spin (DESIGN.md)
- Flask route + integration tests (tests/test_web.py, 6 tests)
- Vercel deploy entry (src/app.py re-export)
- PLAN.md Sprint 3 section + README Sprint 3 section

### Files

```text
src/
├── web_app.py          <- Flask app + routes (entry: python src/web_app.py)
└── app.py              <- Vercel entry, re-exports app

templates/
├── base.html           <- Layout: header nav, footer, modal container
├── index.html          <- Explore: input, chips, search/roulette, loading bar
└── _results_section.html <- Results grid + empty state partial

static/
├── css/style.css       <- Warm culinary theme on top of Tailwind
└── js/app.js           <- fetch search, modal, spin, toast

tests/
└── test_web.py         <- Flask test client tests (6 tests)
```

Note: Sprint1/ Sprint2/ Sprint3/ folders are submission pointers - real code stays in src//templates//static//tests/.

---

[Back to top](#top) | [README](README.md)
