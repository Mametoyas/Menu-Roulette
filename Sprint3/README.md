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
