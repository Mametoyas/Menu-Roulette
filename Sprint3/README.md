<a id="top"></a>

[README](../README.md) | [Members](../MEMBERS.md) | [Plan](../PLAN.md) | [Design](../DESIGN.md) | [Sprint1](../Sprint1/README.md) | [Sprint2](../Sprint2/README.md) | [Sprint3](../Sprint3/README.md) | [Changelog](../CHANGELOG.md) | [Review](../SPRINT_REVIEW.md) | [Peer Eval](../PEER_EVALUATION.md)

# Sprint 3 - Web App and Full-Stack Integration

**Due: 02/10/2569 | Demo: 29-30/09/2569**

## Objective
- Flask web app reusing Sprint 1+2 engine, DESIGN.md UI, async fetch, modal, roulette.

## Deliverables (commit 38657d1..23805a5, 2026-09-20)
- src/web_app.py - Flask routes GET /, POST /api/search, GET /recipe/<id>
- src/app.py - Vercel entry re-export
- templates/base.html, templates/index.html, templates/_results_section.html
- static/css/style.css, static/js/app.js
- tests/test_web.py (6 tests, Flask test client)
- PLAN.md Sprint3 section, README Sprint3 section

## Definition of Done
1. python src/web_app.py opens http://127.0.0.1:5000
2. Search calls real TheMealDB server-side, renders cards + loading bar
3. Card click opens detail modal
4. Roulette picks random and opens modal
5. Async fetch, no full reload
6. PEP8 + pytest pass incl. test_web.py

## Verify
- pytest tests/test_web.py -v
- python src/web_app.py

Full code lives in repo root src//templates//static/ - this folder is the Sprint 3 submission pointer.

## Role-Based Rubrics - Sprint 3 (45 points)

Team: Planner Benz / Coder Toey (routes + backend binding) / Coder Ter (templates + static UI) / Debugger Khong

### Planner (15)

| Criteria | Fair (1-2) | Good (3-4) | Excellent (5) | Max |
|---|---|---|---|---|
| Integration spec and schema | Vague wiring, no state detail | Basic UI-to-BLL map, no edge cases | Full integration spec, state rules, end-to-end DoD | 5 |
| DoD clarity | No measurable DoD | DoD for main flows, no exceptions | Testable DoD incl. normal + error + demo script | 5 |
| PLAN.md docs | Empty or incomplete | Organized and readable | Detailed, professional Markdown with route map | 5 |

### Coder (15)

| Criteria | Fair (1-2) | Good (3-4) | Excellent (5) | Max |
|---|---|---|---|---|
| Layering and wiring | Logic mixed into templates/JS | Flask routes call engine, minor leaks | Thin web layer, all logic reused from engine | 5 |
| State and data consistency | Stale UI, lost selection | Selection/favorites persist per session | Consistent state, no reload, loading + modal correct | 5 |
| Code quality | Bad names, no comments, off PEP8 | Tidy, docstrings, good names | Clean PEP8, docstrings, DESIGN.md followed | 5 |

### Debugger (15)

| Criteria | Fair (1-2) | Good (3-4) | Excellent (5) | Max |
|---|---|---|---|---|
| Edge cases | Happy path only | Basic edge (empty, bad input, 404) | Full cover (empty, invalid, API fail, modal, roulette) | 5 |
| Exception resilience | Unhandled crash or blank page | try-except + JSON error status | Full handling with toast/modal/empty-state feedback | 5 |
| Bug report and PR | Unclear PR, no repro steps | Clear bugs, good PR | Systematic Observation/Expected/Actual + clean PR | 5 |

Backlinks: ../README.md (index) / ../MEMBERS.md (team) / ../SPRINT_REVIEW.md (QA) / ../PEER_EVALUATION.md (peer form)

---

[Back to top](#top) | [README](../README.md)

AI log ฉบับเต็มของ Sprint นี้: [LEARNINGLOG.md](LEARNINGLOG.md)
