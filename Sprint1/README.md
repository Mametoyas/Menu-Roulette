<a id="top"></a>

[README](../README.md) | [Members](../MEMBERS.md) | [Plan](../PLAN.md) | [Design](../DESIGN.md) | [Sprint1](../Sprint1/README.md) | [Sprint2](../Sprint2/README.md) | [Sprint3](../Sprint3/README.md) | [Changelog](../CHANGELOG.md) | [Review](../SPRINT_REVIEW.md) | [Peer Eval](../PEER_EVALUATION.md)

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

## Role-Based Rubrics - Sprint 1 (45 points)

Team: Planner Benz / Coder Toey / Coder Ter / Debugger Khong

### Planner (15)

| Criteria | Fair (1-2) | Good (3-4) | Excellent (5) | Max |
|---|---|---|---|---|
| Planning and scope | Vague spec, coder cannot start | Basic features defined, some detail missing | Full spec, coder can build immediately | 5 |
| Definition of Done | No done conditions | DoD for main features, no edge cases | Clear DoD incl. normal + error paths | 5 |
| PLAN.md docs | Missing or incomplete | Complete and readable | Well-structured, valid Markdown | 5 |

### Coder (15)

| Criteria | Fair (1-2) | Good (3-4) | Excellent (5) | Max |
|---|---|---|---|---|
| Code structure | Single block, no functions | Basic split, some overloaded functions | Clean modular split (display/input/main) | 5 |
| Input and control flow | Crashes on bad input | while/if-elif-else works | Full flow with strip/lower guards | 5 |
| Readability | Bad names, no comments | Good names, key comments | Clean code, docstrings, PEP8 | 5 |

### Debugger (15)

| Criteria | Fair (1-2) | Good (3-4) | Excellent (5) | Max |
|---|---|---|---|---|
| Edge cases | Happy path only | Basic bad input incl. case | Full cover (non-numeric, mixed case, spaces) | 5 |
| Exception handling | No try-except, crash | try-except ValueError present | try-except with re-prompt loop | 5 |
| Report and PR | No report or messy PR | Clear report with Wow/Whoops | Observation/Expected/Actual + clean PR | 5 |

Backlinks: ../README.md (index) / ../MEMBERS.md (team) / ../SPRINT_REVIEW.md (QA) / ../PEER_EVALUATION.md (peer form)

---

[Back to top](#top) | [README](../README.md)
