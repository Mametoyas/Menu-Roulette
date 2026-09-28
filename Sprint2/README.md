<a id="top"></a>

[README](../README.md) | [Members](../MEMBERS.md) | [Plan](../PLAN.md) | [Design](../DESIGN.md) | [Sprint1](../Sprint1/README.md) | [Sprint2](../Sprint2/README.md) | [Sprint3](../Sprint3/README.md) | [Changelog](../CHANGELOG.md) | [Review](../SPRINT_REVIEW.md) | [Peer Eval](../PEER_EVALUATION.md)

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

## Role-Based Rubrics - Sprint 2 (45 points)

Team: Planner Toey / Coder Khong (api_client) / Coder Benz (engine) / Debugger Ter

### Planner (15)

| Criteria | Fair (1-2) | Good (3-4) | Excellent (5) | Max |
|---|---|---|---|---|
| Architecture and schema | Vague, no file/DB detail | Basic classes + file layout, no edge cases | Full UML, schema, module bounds | 5 |
| DoD clarity | No measurable DoD | DoD for main funcs, no exceptions | Testable DoD incl. normal + error states | 5 |
| PLAN.md docs | Empty or incomplete | Organized and readable | Detailed, professional Markdown | 5 |

### Coder (15)

| Criteria | Fair (1-2) | Good (3-4) | Excellent (5) | Max |
|---|---|---|---|---|
| OOP and layering | Procedural single file, no OOP | Classes used but logic leaks into UI | Clean split: presentation / logic / data access | 5 |
| Algorithm and persistence | Wrong results or corrupt files | Search/sort + File I/O correct | Efficient algorithm, full I/O handling | 5 |
| Code quality | Bad names, no comments, off PEP8 | Tidy, docstrings, good names | Clean PEP8, docstrings everywhere | 5 |

### Debugger (15)

| Criteria | Fair (1-2) | Good (3-4) | Excellent (5) | Max |
|---|---|---|---|---|
| Edge cases | Happy path only | Basic edge (empty, wrong type) | Full cover (corrupt file, concurrency, bounds) | 5 |
| Exception resilience | Unhandled crash | Basic try-except | Full try-except with user-friendly alerts | 5 |
| Bug report and PR | Unclear PR, no repro steps | Clear bugs, good PR | Systematic Observation/Expected/Actual + clean PR | 5 |

Backlinks: ../README.md (index) / ../MEMBERS.md (team) / ../SPRINT_REVIEW.md (QA) / ../PEER_EVALUATION.md (peer form)

---

[Back to top](#top) | [README](../README.md)
