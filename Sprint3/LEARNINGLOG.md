<a id="top"></a>

[README](../README.md) | [Members](../MEMBERS.md) | [Plan](../PLAN.md) | [Design](../DESIGN.md) | [Sprint1](../Sprint1/README.md) | [Sprint2](../Sprint2/README.md) | [Sprint3](../Sprint3/README.md) | [Changelog](../CHANGELOG.md) | [Review](../SPRINT_REVIEW.md) | [Peer Eval](../PEER_EVALUATION.md) | [AI Log S1](../Sprint1/LEARNINGLOG.md) | [AI Log S2](../Sprint2/LEARNINGLOG.md)

# ประวัติการใช้ AI - Sprint 3 (AI Usage Log)

โปรเจกต์: Recipe Roulette (TheMealDB) | ช่วงงาน: 20/09/2569 (ส่ง 02/10/2569) | ทีมตาม PLAN/Readme: Benz Planner / Toey Coder (routes) / Ter Coder (UI) / Khong Debugger (tests)


### Step 1: วางแผน Sprint 3 (ผู้รับผิดชอบ: Benz, Planner)

**User Prompt:**
> ช่วยวาง Sprint 3 หน่อย เอา Flask ห่อ engine Sprint 1+2 แบบไม่แตะ logic ขอ route GET / POST /api/search GET /recipe/<id> หน้า Explore มี chips loading modal roulette ตาม DESIGN.md

**AI Response:**
AI เสนอ thin presentation layer เรียก run_roulette_simulation ตรง async fetch ไม่ reload ทีมนำไปเขียน PLAN.md ช่วง Sprint 3 เอง

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** ยึด DoD 6 ข้อ (เปิด 127.0.0.1:5000 / การ์ด / modal / roulette / async / pytest ผ่าน)

### Step 2: เพิ่ม format_recipe + ผูก main.py (ผู้รับผิดชอบ: Toey, Coder)

**User Prompt:**
> เพิ่ม format_recipe ใน engine หน่อย map strMeal/strCategory/strArea/strMealThumb/strInstructions/strYoutube + ingredients + score คง score ผ่านมาด้วย แล้วแก้ main.py ให้ format ทั้ง top_recipes และ selected_recipe เป็น GUI-ready dict

**AI Response:**
AI อธิบาย mapping พร้อมโค้ดฟังก์ชันด้านล่าง (ส่วนนี้คือ +19 บรรทัดของ commit 38657d1 ส่วนอื่นของ engine อยู่ใน log Sprint 2 แล้ว)

```python
# src/recipe_engine.py - เฉพาะส่วนที่เพิ่ม Sprint 3 (บรรทัด 155-171)
def format_recipe(meal: Dict) -> Dict:
    """Converts a TheMealDB meal dict into a GUI-friendly display dict.

    Maps raw API fields (strMeal, strInstructions, strMealThumb ...) to
    friendly keys ready for rendering in a GUI.
    """
    return {
        "id": meal.get("idMeal"),
        "name": meal.get("strMeal"),
        "category": meal.get("strCategory"),
        "area": meal.get("strArea"),
        "image_url": meal.get("strMealThumb") or "",
        "ingredients": extract_ingredients(meal),
        "instructions": meal.get("strInstructions") or "",
        "youtube_url": meal.get("strYoutube") or "",
        "score": meal.get("score"),
    }
```

```python
# src/main.py - ทั้งไฟล์ (ผูก format ทั้ง top และ selected)
"""Console entry point — Sprint 2 live TheMealDB API flow, GUI-ready output."""

import json

# Import supports both execution modes:
#   python src/main.py      -> utils / recipe_engine / api_client (src/ on sys.path)
#   pytest (pythonpath = .) -> src.utils / src.recipe_engine / src.api_client
try:  # pragma: no cover - exercised when running `python src/main.py`
    from utils import clean_ingredient_input, InvalidIngredientError
    from recipe_engine import filter_and_rank, pick_random_recipe, format_recipe
    from api_client import APIError
except ImportError:
    from src.utils import clean_ingredient_input, InvalidIngredientError
    from src.recipe_engine import filter_and_rank, pick_random_recipe, format_recipe
    from src.api_client import APIError


def run_roulette_simulation(raw_input: str) -> dict:
    """Executes: Clean -> Live API Search/Score/Rank -> Format -> Random Pick.

    Returns a GUI-ready result dict; every recipe is passed through
    format_recipe() so fields are already human/friendly named.
    """
    try:
        cleaned_ingredients = clean_ingredient_input(raw_input)
        ranked = filter_and_rank(cleaned_ingredients)
        selected = pick_random_recipe(ranked)

        return {
            "status": "success",
            "query": cleaned_ingredients,
            "match_count": len(ranked),
            "selected_recipe": format_recipe(selected) if selected else None,
            "top_recipes": [format_recipe(meal) for meal in ranked],
        }
    except InvalidIngredientError as e:
        return {"status": "error", "message": str(e)}
    except APIError as e:
        return {"status": "error", "message": str(e)}


def run_console() -> None:
    """Runs the interactive input()/print() roulette session."""
    sample_query = input("Enter the ingredients (example: 'Pork, Garlic'):")
    result = run_roulette_simulation(sample_query)
    print("Execution Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":  # pragma: no cover
    run_console()
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** เทส format 3 เคสใน test_engine (ดู Step 6)

### Step 3: เขียน src/web_app.py + src/app.py (ผู้รับผิดชอบ: Toey, Coder) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน Flask web_app.py หน่อย route GET / เรนเดอร์ index, POST /api/search รับ JSON ingredients ยิง run_roulette_simulation, GET /recipe/<id> คืน format_recipe (404 ถ้าไม่เจอ) anchor template/static ที่ repo root ให้รันได้ทั้ง python src/web_app.py และ pytest ส่วน app.py ให้ re-export app เฉยๆ ไว้ให้ Vercel

**AI Response:**
AI อธิบาย 3 routes + PROJECT_ROOT anchor + QUICK_CHIPS พร้อมโค้ด 2 ไฟล์ด้านล่าง

```python
# src/web_app.py - ทั้งไฟล์
"""Flask web application for Recipe Roulette — Sprint 3 web UI.

Run with:  python src/web_app.py
Open:      http://127.0.0.1:5000

The web layer is a thin presentation wrapper around the pure back-end
engine (main -> recipe_engine + api_client). Recipes, scoring, random
selection all reuse Sprint 1 & 2 modules.
"""

from pathlib import Path

from flask import Flask, jsonify, render_template, request

try:
    from api_client import get_meal_by_id
    from main import run_roulette_simulation
    from recipe_engine import format_recipe
except ImportError:
    from src.api_client import get_meal_by_id
    from src.main import run_roulette_simulation
    from src.recipe_engine import format_recipe

# Anchor app to the repository root so templates/ and static/ resolve in
# both `python src/web_app.py` and pytest execution modes.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / "templates"),
    static_folder=str(PROJECT_ROOT / "static"),
)
app.json.ensure_ascii = False

# Ingredient suggestions rendered as quick-pick chips (DESIGN.md §8).
QUICK_CHIPS = [
    "chicken",
    "pork",
    "beef",
    "shrimp",
    "egg",
    "rice",
    "garlic",
    "onion",
    "soy sauce",
    "tofu",
]


@app.context_processor
def inject_globals() -> dict:
    """Injects shared values into every template."""
    return {"quick_chips": QUICK_CHIPS}


@app.route("/")
def index():
    """Explore page — hero, quick chips, ingredient input, results."""
    return render_template("index.html")


@app.route("/api/search", methods=["POST"])
def api_search():
    """Runs the full back-end roulette pipeline and returns JSON."""
    payload = request.get_json(silent=True) or {}
    result = run_roulette_simulation(payload.get("ingredients", ""))
    return jsonify(result)


@app.route("/recipe/<meal_id>")
def recipe_detail(meal_id):
    """Returns a single formatted recipe as JSON (detail / modal data)."""
    meal = get_meal_by_id(meal_id)
    if meal is None:
        return jsonify({"error": "Recipe not found"}), 404
    return jsonify(format_recipe(meal))


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True, host="127.0.0.1", port=5000)
```

```python
# src/app.py - ทั้งไฟล์
"""Vercel entry point.

Vercel auto-detects Flask by looking for a module-level ``app`` instance in a
recognized entry file (src/app.py). Keep this file minimal — it only re-exports
the real Flask app from web_app.py so routing stays unchanged.
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from web_app import app  # noqa: E402
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** แก้ path แตกต่างระหว่างรันตรงกับ pytest ด้วย PROJECT_ROOT (ดู SPRINT_REVIEW Whoops Sprint 3)

### Step 4: เขียน templates 3 ไฟล์ (ผู้รับผิดชอบ: Ter, Coder) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน templates หน่อย base.html (layout + header/footer + modal/toast container + Tailwind/Kanit/FontAwesome), index.html (hero + input + quick chips + selected + search/roulette + loading bar), _results_section.html (grid + empty state) ตาม DESIGN.md

**AI Response:**
AI ให้ 3 ไฟล์ด้านล่าง

```html
<!-- templates/base.html - ทั้งไฟล์ -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Recipe Roulette{% endblock %}</title>
    <meta name="description" content="Recipe Roulette — find and randomly recommend recipes from the ingredients in your fridge.">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body class="bg-amber-50/40 min-h-screen flex flex-col text-slate-600">

    <header class="sticky top-0 z-40 bg-white/80 backdrop-blur-md border-b border-amber-100 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-3">
            <a href="/" class="flex items-center gap-2.5 group min-w-0" aria-label="Recipe Roulette home">
                <span class="w-10 h-10 shrink-0 rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center text-white shadow-md shadow-amber-500/30 group-hover:scale-105 transition-transform">
                    <i class="fa-solid fa-utensils"></i>
                </span>
                <span class="text-lg sm:text-xl font-extrabold bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent truncate">Recipe Roulette</span>
            </a>

            <nav class="flex items-center gap-1 sm:gap-2" aria-label="Main navigation">
                <a href="/" class="nav-tab {{ 'active' if request.endpoint == 'index' else '' }}">
                    <i class="fa-solid fa-compass"></i><span class="nav-label">Explore</span>
                </a>
            </nav>
        </div>
    </header>

    <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {% block content %}{% endblock %}
    </main>

    <footer class="border-t border-amber-100 mt-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-2 text-sm text-slate-400">
            <span><i class="fa-solid fa-utensils text-amber-500"></i> Recipe Roulette — powered by TheMealDB</span>
            <span>Sprint 3 &middot; Web App</span>
        </div>
    </footer>

    <div id="recipe-modal" class="hidden fixed inset-0 z-[70] overflow-y-auto p-4 flex items-center justify-center" role="dialog" aria-modal="true"></div>

    <div id="toast" class="fixed bottom-6 left-1/2 z-[80] -translate-x-1/2 px-5 py-3 rounded-xl text-white text-sm font-semibold shadow-xl opacity-0 pointer-events-none transition-all duration-300 translate-y-2" role="status"></div>

    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

```html
<!-- templates/index.html - ทั้งไฟล์ -->
{% extends "base.html" %}
{% block title %}Recipe Roulette — find recipes by your ingredients{% endblock %}

{% block content %}

<section class="text-center py-6 sm:py-10 space-y-3">
    <span class="inline-flex items-center gap-2 text-xs font-bold tracking-wide text-amber-700 bg-amber-100/70 border border-amber-200 rounded-full px-3 py-1">
        <i class="fa-solid fa-wand-magic-sparkles"></i> RANDOM RECIPE FINDER
    </span>
    <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-800 leading-tight max-w-3xl mx-auto">
        What's in your fridge <span class="bg-gradient-to-r from-amber-500 to-orange-600 bg-clip-text text-transparent">today?</span>
    </h1>
    <p class="text-slate-500 max-w-xl mx-auto text-sm sm:text-base">
        Drop your ingredients, spin the roulette, and cook exactly what you crave — no more &ldquo;what should I eat?&rdquo;
    </p>
</section>

<section class="bg-white shadow-2xl shadow-amber-100/60 rounded-2xl p-5 sm:p-6 space-y-4">
    <div class="flex flex-col sm:flex-row gap-3">
        <div class="flex-1 flex items-center gap-3 bg-slate-50 rounded-xl px-4 py-3 focus-within:ring-2 focus-within:ring-amber-400 transition">
            <i class="fa-solid fa-carrot text-amber-500"></i>
            <input id="ingredient-input" type="text" autocomplete="off"
                   placeholder="e.g. pork, garlic, soy sauce"
                   class="flex-1 bg-transparent outline-none placeholder-slate-400 text-sm sm:text-base text-slate-700">
        </div>
        <button id="add-ingredient" class="px-5 py-3 rounded-xl bg-slate-100 hover:bg-amber-100 text-slate-600 hover:text-amber-700 font-semibold text-sm transition active:scale-95">
            <i class="fa-solid fa-plus"></i> Add
        </button>
    </div>

    <div class="flex items-center gap-2 overflow-x-auto pb-1" id="quick-chips">
        <span class="shrink-0 text-xs font-bold text-slate-400 uppercase tracking-wide">Try:</span>
        {% for chip in quick_chips %}
        <button class="quick-chip shrink-0 bg-slate-100 hover:bg-amber-100 text-slate-600 text-sm px-3 py-1.5 rounded-full transition active:scale-95"
                data-ingredient="{{ chip }}" type="button">
            <i class="fa-solid fa-circle-plus text-[10px]"></i> {{ chip }}
        </button>
        {% endfor %}
    </div>

    <div id="selected-ingredients" class="flex flex-wrap gap-2 min-h-[2rem]" aria-label="Selected ingredients"></div>

    <div class="flex flex-col sm:flex-row gap-3 pt-1">
        <button id="search-btn" type="button"
                class="flex-1 flex items-center justify-center gap-2 px-5 py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-bold shadow-md shadow-emerald-500/25 hover:brightness-110 hover:shadow-lg active:scale-95 transition">
            <i class="fa-solid fa-magnifying-glass"></i> Search Recipes
        </button>
        <button id="roulette-btn" type="button"
                class="flex-1 flex items-center justify-center gap-2 px-5 py-3.5 rounded-xl bg-gradient-to-r from-amber-500 to-orange-600 text-white font-bold shadow-md shadow-amber-500/30 hover:brightness-110 hover:shadow-lg active:scale-95 transition">
            <i class="fa-solid fa-arrows-spin"></i> Spin the Roulette
        </button>
    </div>

    <div id="loading-bar" class="hidden pt-3" role="status" aria-live="polite">
        <div class="flex items-center justify-center gap-2 text-sm text-slate-500">
            <i class="fa-solid fa-arrows-spin loading-spin text-amber-500"></i>
            <span id="loading-text">Searching recipes...</span>
        </div>
        <div class="mt-2 h-1.5 w-full rounded-full bg-slate-100 overflow-hidden">
            <div class="loading-progress h-full rounded-full"></div>
        </div>
    </div>
</section>

{% include "_results_section.html" %}

{% endblock %}
```

```html
<!-- templates/_results_section.html - ทั้งไฟล์ -->
<section id="results-section" class="hidden space-y-6">
    <div class="flex items-center justify-between flex-wrap gap-2">
        <h2 id="results-title" class="text-xl sm:text-2xl font-bold text-slate-800"></h2>
        <div class="flex items-center gap-2 flex-wrap">
            <span id="results-count" class="text-sm font-semibold text-slate-500 bg-white border border-slate-200 rounded-full px-3 py-1"></span>
            <button id="clear-results" type="button"
                    class="hidden text-xs font-semibold text-slate-400 hover:text-rose-500 transition">
                <i class="fa-solid fa-rotate-left"></i> Clear
            </button>
        </div>
    </div>
    <div id="results-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"></div>
</section>

<section id="empty-state" class="hidden text-center py-16 space-y-4">
    <div class="w-20 h-20 mx-auto rounded-full bg-white shadow-inner flex items-center justify-center text-slate-300 text-3xl">
        <i class="fa-solid fa-bowl-food"></i>
    </div>
    <div>
        <h3 class="text-lg font-bold text-slate-600">No recipes found</h3>
        <p class="text-sm text-slate-400">Try different ingredients, or check your spelling.</p>
    </div>
</section>
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** ตรวจ responsive + modal/loading ตาม DoD Sprint 3

### Step 5: เขียน static/css/style.css + static/js/app.js (ผู้รับผิดชอบ: Ter, Coder) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน static หน่อย style.css (Kanit + nav/loading/chips/cards/modal/toast/roulette-spin ตาม DESIGN.md ทับ Tailwind) กับ app.js (chips state, fetch POST /api/search, render การ์ด, modal, roulette auto-open, loading, toast, escapeHtml กัน XSS)

**AI Response:**
AI ให้ 2 ไฟล์ด้านล่าง

```css
/* static/css/style.css - ทั้งไฟล์ */
/* Recipe Roulette — Sprint 3 custom styles on top of Tailwind CDN.
   Follows DESIGN.md: warm culinary theme, soft shadows, glassmorphism. */

:root {
  --amber-500: #f59e0b;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: "Kanit", system-ui, -apple-system, "Segoe UI", sans-serif;
}

/* ---------- Navigation (DESIGN.md §7) ---------- */
.nav-tab {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
  transition: background-color 0.2s ease, color 0.2s ease, transform 0.15s ease;
}

.nav-tab:hover {
  background: #fffbeb;
  color: #b45309;
}

.nav-tab:active {
  transform: scale(0.96);
}

.nav-tab.active {
  background: #fffbeb;
  color: #b45309;
}

@media (max-width: 640px) {
  .nav-label {
    display: none;
  }
}

/* ---------- Loading progress (below Search bar) ---------- */
.loading-spin {
  animation: loading-spin 0.9s linear infinite;
}

@keyframes loading-spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-progress {
  width: 40%;
  background: linear-gradient(90deg, #f59e0b, #f97316, #10b981);
  animation: loading-slide 1.1s ease-in-out infinite;
}

@keyframes loading-slide {
  0% {
    margin-left: -40%;
  }
  100% {
    margin-left: 100%;
  }
}

/* ---------- Chips & badges ---------- */
.select-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--amber-500);
  color: #fff;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 0.4rem 0.85rem;
  border-radius: 9999px;
  box-shadow: 0 2px 6px rgba(245, 158, 11, 0.25);
  animation: fade-enter 0.25s ease;
}

.select-chip .fa-xmark {
  cursor: pointer;
  opacity: 0.85;
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.select-chip .fa-xmark:hover {
  opacity: 1;
  transform: scale(1.2);
}

/* ---------- Cards (DESIGN.md §9) ---------- */
.recipe-card {
  transition: box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.recipe-card:hover {
  transform: translateY(-2px);
}

.line-clamp-1,
.line-clamp-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-1 {
  -webkit-line-clamp: 1;
}

.line-clamp-2 {
  -webkit-line-clamp: 2;
}

/* ---------- Quick chips scrollbar (DESIGN.md §8) ---------- */
#quick-chips::-webkit-scrollbar {
  height: 4px;
}

#quick-chips::-webkit-scrollbar-thumb {
  background: #fed7aa;
  border-radius: 9999px;
}

#quick-chips::-webkit-scrollbar-track {
  background: transparent;
}

/* ---------- Roulette spin (DESIGN.md §14) ---------- */
.roulette-spin {
  animation: roulette-spin 1.2s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes roulette-spin {
  0% {
    transform: rotate(0deg) scale(1);
  }
  50% {
    transform: rotate(180deg) scale(1.15);
  }
  100% {
    transform: rotate(360deg) scale(1);
  }
}

/* ---------- Modal (DESIGN.md §15) ---------- */
.modal-enter {
  animation: modal-enter 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes modal-enter {
  from {
    opacity: 0;
    transform: translateY(24px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.fade-enter {
  animation: fade-enter 0.3s ease;
}

@keyframes fade-enter {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* ---------- Toast ---------- */
#toast.success {
  background: linear-gradient(90deg, #10b981, #0d9488);
}

#toast.danger {
  background: linear-gradient(90deg, #f43f5e, #e11d48);
}

#toast.visible {
  opacity: 1;
  transform: translateY(0);
}
```

```javascript
// static/js/app.js - ทั้งไฟล์
/* Recipe Roulette — Sprint 3 client interactivity.
   Implemented against the API contract in src/web_app.py.
   UI follows DESIGN.md (recipe cards, modal, roulette spin, toasts). */
(function () {
  "use strict";

  var $ = function (sel, root) {
    return (root || document).querySelector(sel);
  };
  var $$ = function (sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  };

  var registry = {}; // id -> formatted recipe, used by shared click handlers
  var state = {
    query: [], // selected ingredients / chips
  };

  var PLACEHOLDER = "data:image/svg+xml;utf8," + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">' +
    '<rect width="100%" height="100%" fill="#fef3c7"/>' +
    '<text x="50%" y="50%" font-family="Arial" font-size="20" fill="#d97706" ' +
    'text-anchor="middle">No image</text></svg>'
  );

  /* ---------- utilities ---------- */

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  window.fallbackImg = function (img) {
    img.onerror = null;
    img.src = PLACEHOLDER;
  };

  function imgHtml(url, alt) {
    if (!url) {
      return '<div class="w-full h-full bg-gradient-to-br from-amber-100 to-orange-100 ' +
        'flex items-center justify-center text-amber-400 text-4xl">' +
        '<i class="fa-solid fa-utensils"></i></div>';
    }
    return '<img src="' + escapeHtml(url) + '" alt="' + escapeHtml(alt) + '" loading="lazy" ' +
      'class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-300" ' +
      'onerror="window.fallbackImg && fallbackImg(this)">';
  }

  function api(url, options) {
    return fetch(url, options).then(function (resp) {
      return resp.json();
    });
  }

  function postPayload(body) {
    return {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    };
  }

  /* ---------- toast ---------- */

  var toastTimer = null;

  function showToast(message, type) {
    var toast = $("#toast");
    if (!toast) return;
    toast.textContent = message;
    toast.className = "fixed bottom-6 left-1/2 z-[80] -translate-x-1/2 px-5 py-3 " +
      "rounded-xl text-white text-sm font-semibold shadow-xl transition-all " +
      "duration-300 translate-y-2 " + (type === "danger" ? "danger" : "success") + " visible";
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toast.className = "fixed bottom-6 left-1/2 z-[80] -translate-x-1/2 px-5 py-3 " +
        "rounded-xl text-white text-sm font-semibold shadow-xl transition-all " +
        "duration-300 translate-y-2 opacity-0 pointer-events-none";
    }, 2600);
  }

  /* ---------- loading progress (below Search bar) ---------- */

  var loading = false;

  function showLoading(message) {
    var text = $("#loading-text");
    if (text && message) text.textContent = message;
    var bar = $("#loading-bar");
    if (bar) bar.classList.remove("hidden");
    loading = true;
  }

  function hideLoading() {
    var bar = $("#loading-bar");
    if (bar) bar.classList.add("hidden");
    loading = false;
  }

  /* ---------- ingredient chips (Explore) ---------- */

  function addSelectedChip(name) {
    if (state.query.indexOf(name) !== -1) return;
    state.query.push(name);
    var container = $("#selected-ingredients");
    var chip = document.createElement("span");
    chip.className = "select-chip";
    chip.dataset.value = name;
    chip.innerHTML = "<span>" + escapeHtml(name) + "</span>" +
      '<i class="fa-solid fa-xmark" role="button" aria-label="Remove"></i>';
    chip.querySelector(".fa-xmark").addEventListener("click", function () {
      state.query = state.query.filter(function (item) {
        return item !== name;
      });
      chip.remove();
    });
    container.appendChild(chip);
  }

  function readInput() {
    var input = $("#ingredient-input");
    return input ? input.value.trim() : "";
  }

  function addFromInput() {
    var value = readInput();
    if (!value) {
      showToast("Type an ingredient first", "danger");
      return;
    }
    value.split(",").forEach(function (part) {
      var cleaned = part.trim().toLowerCase();
      if (cleaned) addSelectedChip(cleaned);
    });
    var input = $("#ingredient-input");
    if (input) input.value = "";
  }

  /* ---------- results rendering ---------- */

  function matchedIngredientTags(recipe) {
    var matched = new Set(state.query);
    var shown = recipe.ingredients || [];
    return shown.slice(0, 4).map(function (ing) {
      var hit = matched.has(ing);
      var cls = hit
        ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
        : "bg-slate-100 text-slate-500";
      var icon = hit
        ? '<i class="fa-solid fa-check"></i>'
        : '<i class="fa-solid fa-leaf"></i>';
      return '<span class="inline-flex items-center gap-1 text-[11px] px-2 py-1 rounded-full ' + cls + '">' +
        icon + " " + escapeHtml(ing) + "</span>";
    }).join("");
  }

  function recipeCardHtml(recipe) {
    var pct = recipe.score != null ? Math.round(recipe.score * 100) : null;
    var badge = pct != null
      ? '<span class="absolute bottom-2 left-2 bg-emerald-500 text-white text-xs font-bold px-2 py-1 rounded-lg">' +
        pct + "% match</span>"
      : "";
    return '<article class="recipe-card group bg-white rounded-2xl overflow-hidden shadow-md ' +
      'hover:shadow-xl transition-all duration-300 cursor-pointer" data-id="' + escapeHtml(recipe.id) + '">' +
      '<div class="relative h-48 overflow-hidden">' +
      imgHtml(recipe.image_url, recipe.name) +
      '<span class="absolute top-2 left-2 bg-slate-900/60 backdrop-blur-md text-white text-xs px-2 py-1 rounded-lg">' +
      escapeHtml(recipe.area || recipe.category || "Recipe") + "</span>" +
      badge +
      "</div>" +
      '<div class="p-4 space-y-2">' +
      '<div class="flex items-center gap-2 text-xs text-slate-400">' +
      '<span class="bg-amber-50 text-amber-700 px-2 py-0.5 rounded-full font-medium">' +
      escapeHtml(recipe.category || "Recipe") + "</span>" +
      '<span class="flex items-center gap-1"><i class="fa-solid fa-star text-amber-400"></i> 4.5</span>' +
      "</div>" +
      '<h3 class="font-bold text-slate-800 line-clamp-1">' + escapeHtml(recipe.name) + "</h3>" +
      '<div class="flex flex-wrap gap-1.5 pt-1">' + matchedIngredientTags(recipe) + "</div>" +
      "</div></article>";
  }

  function renderResults(data) {
    var section = $("#results-section");
    var empty = $("#empty-state");
    var grid = $("#results-grid");
    var count = $("#results-count");
    var title = $("#results-title");
    var clearBtn = $("#clear-results");

    if (!grid) return;

    if (data.status === "error") {
      section.classList.add("hidden");
      empty.classList.remove("hidden");
      title.textContent = "Something went wrong";
      count.textContent = "";
      showToast(data.message || "Search failed", "danger");
      return;
    }

    registry = {};
    (data.top_recipes || []).forEach(function (r) {
      registry[String(r.id)] = r;
    });

    var total = data.top_recipes ? data.top_recipes.length : 0;
    section.classList.remove("hidden");
    empty.classList.add("hidden");
    title.textContent = total ? "Matched Recipes" : "No Recipes";
    count.textContent = total
      ? total + " matching recipe" + (total > 1 ? "s" : "") + " for: " + state.query.join(", ")
      : "";
    clearBtn.classList.toggle("hidden", total === 0);

    grid.innerHTML = (data.top_recipes || []).map(recipeCardHtml).join("");
    attachCardHandlers(grid);

    if (total === 0) {
      section.classList.add("hidden");
      empty.classList.remove("hidden");
    }
  }

  /* ---------- shared card / modal handlers ---------- */

  function attachCardHandlers(grid) {
    grid.addEventListener("click", function (e) {
      var card = e.target.closest(".recipe-card");
      if (!card) return;
      openModal(registry[card.dataset.id]);
    });
  }

  function openModal(recipe) {
    if (!recipe) return;
    var overlay = $("#recipe-modal");
    overlay.innerHTML = modalHtml(recipe);
    overlay.classList.remove("hidden");
    overlay.classList.add("flex");
    document.body.style.overflow = "hidden";

    $$(".modal-close", overlay).forEach(function (btn) {
      btn.addEventListener("click", closeModal);
    });

    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) closeModal();
    });

    $$(".ingredient-item", overlay).forEach(function (item) {
      item.addEventListener("click", function () {
        item.classList.toggle("checked");
      });
    });

    document.addEventListener("keydown", onModalKeydown);
  }

  function onModalKeydown(e) {
    if (e.key === "Escape") closeModal();
  }

  function closeModal() {
    var overlay = $("#recipe-modal");
    overlay.classList.add("hidden");
    overlay.classList.remove("flex");
    overlay.innerHTML = "";
    document.body.style.overflow = "";
    document.removeEventListener("keydown", onModalKeydown);
  }

  function modalHtml(recipe) {
    var pct = recipe.score != null ? Math.round(recipe.score * 100) : null;
    var banner = pct != null
      ? '<div class="flex items-center gap-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 ' +
        'text-white px-4 py-3 shadow-md shadow-emerald-500/20 fade-enter">' +
        '<i class="fa-solid fa-circle-check text-lg"></i>' +
        '<div><p class="text-sm font-bold">' + pct + "% ingredient match</p>" +
        '<p class="text-xs opacity-80">A great recipe for your fridge</p></div></div>'
      : "";

    var ingredients = (recipe.ingredients || []).map(function (ing) {
      return '<li class="ingredient-item flex items-start gap-3 cursor-pointer rounded-lg p-1.5 -m-1.5 hover:bg-amber-50/60 transition">' +
        '<span class="mt-0.5 w-5 h-5 shrink-0 rounded-md border border-slate-200 flex items-center justify-center">' +
        '<i class="fa-solid fa-check text-emerald-500 opacity-0 transition"></i></span>' +
        '<span class="text-sm text-slate-700">' + escapeHtml(ing) + "</span></li>";
    }).join("") || '<li class="text-sm text-slate-400">No ingredients listed.</li>';

    var steps = (recipe.instructions || "")
      .split("\n")
      .map(function (s) { return s.trim(); })
      .filter(Boolean)
      .map(function (s, i) {
        return '<li class="flex gap-3"><span class="shrink-0 w-6 h-6 rounded-full bg-amber-100 ' +
          'text-amber-700 text-xs font-bold flex items-center justify-center">' + (i + 1) + "</span>" +
          '<span class="text-sm text-slate-600">' + escapeHtml(s) + "</span></li>";
      }).join("");

    var youtube = recipe.youtube_url
      ? '<a href="' + escapeHtml(recipe.youtube_url) + '" target="_blank" rel="noopener" ' +
        'class="inline-flex items-center gap-2 text-sm font-semibold text-rose-600 hover:text-rose-500 transition">' +
        '<i class="fa-brands fa-youtube"></i> Watch on YouTube</a>'
      : "";

    return '<div class="modal-enter relative bg-white max-w-2xl w-full rounded-3xl overflow-hidden ' +
      "shadow-2xl max-h-[90vh] flex flex-col\">" +
      '<div class="relative h-56 sm:h-64 shrink-0">' +
      imgHtml(recipe.image_url, recipe.name) +
      '<button type="button" class="modal-close absolute top-3 right-3 w-9 h-9 rounded-full ' +
      'bg-white/90 backdrop-blur-md flex items-center justify-center text-slate-600 ' +
      'hover:text-rose-500 hover:rotate-90 transition" aria-label="Close"><i class="fa-solid fa-xmark"></i></button>' +
      '<div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-slate-900/90 via-slate-900/50 to-transparent p-5 pt-14">' +
      '<h3 class="text-xl sm:text-2xl font-extrabold text-white line-clamp-2">' + escapeHtml(recipe.name) + "</h3>" +
      '<div class="flex items-center gap-2 mt-1 flex-wrap">' +
      '<span class="bg-white/20 backdrop-blur-md text-white text-xs px-2 py-0.5 rounded-full">' +
      escapeHtml(recipe.area || "") + "</span>" +
      '<span class="bg-amber-400/90 text-slate-800 text-xs px-2 py-0.5 rounded-full font-semibold">' +
      escapeHtml(recipe.category || "Recipe") + "</span></div></div></div>" +

      '<div class="overflow-y-auto p-5 space-y-5">' + banner +

      '<div><h4 class="font-bold text-slate-800 mb-3 flex items-center gap-2">' +
      '<i class="fa-solid fa-egg text-amber-500"></i> Ingredients</h4>' +
      '<ul class="grid grid-cols-1 sm:grid-cols-2 gap-2">' + ingredients + "</ul></div>" +

      '<div><h4 class="font-bold text-slate-800 mb-3 flex items-center gap-2">' +
      '<i class="fa-solid fa-list-ol text-orange-500"></i> Instructions</h4>' +
      '<ol class="space-y-3">' + (steps || '<li class="text-sm text-slate-400">No instructions available.</li>') +
      "</ol></div>" +
      (youtube ? '<div class="flex justify-center">' + youtube + "</div>" : "") +
      "</div>" +

      '<div class="p-4 border-t border-slate-100 flex justify-end">' +
      '<button type="button" class="modal-close px-5 py-3 rounded-xl bg-slate-800 text-white text-sm font-bold ' +
      'hover:bg-slate-700 transition active:scale-95">Close</button></div></div>';
  }

  /* ---------- search / roulette ---------- */

  function collectQuery() {
    return state.query.join(", ");
  }

  function runSearch() {
    if (loading) return;
    if (!state.query.length) {
      showToast("Add at least one ingredient first", "danger");
      return;
    }
    showLoading("Searching recipes...");
    api("/api/search", postPayload({ ingredients: collectQuery() }))
      .then(renderResults)
      .catch(function () {
        showToast("Search failed — is the server running?", "danger");
      })
      .then(hideLoading);
  }

  function spinRoulette() {
    if (loading) return;
    var btn = $("#roulette-btn");
    if (btn) {
      var icon = btn.querySelector(".fa-arrows-spin");
      if (icon) {
        icon.classList.remove("roulette-spin");
        void icon.offsetWidth;
        icon.classList.add("roulette-spin");
      }
    }
    if (!state.query.length) {
      showToast("Add at least one ingredient first", "danger");
      return;
    }
    showLoading("Spinning the roulette...");
    api("/api/search", postPayload({ ingredients: collectQuery() }))
      .then(function (data) {
        renderResults(data);
        if (data.status === "success" && data.selected_recipe) {
          setTimeout(function () {
            openModal(data.selected_recipe);
          }, 400);
        } else if (data.status === "error") {
          showToast(data.message || "Search failed", "danger");
        }
      })
      .catch(function () {
        showToast("Search failed — is the server running?", "danger");
      })
      .then(hideLoading);
  }

  /* ---------- page initialisation ---------- */

  function initExplore() {
    var input = $("#ingredient-input");
    var addBtn = $("#add-ingredient");
    var searchBtn = $("#search-btn");
    var rouletteBtn = $("#roulette-btn");
    var clearBtn = $("#clear-results");

    if (input) input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        addFromInput();
      }
    });
    if (addBtn) addBtn.addEventListener("click", addFromInput);

    $$(".quick-chip").forEach(function (chip) {
      chip.addEventListener("click", function () {
        addSelectedChip(chip.dataset.ingredient);
      });
    });

    if (searchBtn) searchBtn.addEventListener("click", runSearch);
    if (rouletteBtn) rouletteBtn.addEventListener("click", spinRoulette);
    if (clearBtn) clearBtn.addEventListener("click", function () {
      $("#results-section").classList.add("hidden");
      $("#empty-state").classList.add("hidden");
      $("#results-grid").innerHTML = "";
      state.query = [];
      var selected = $("#selected-ingredients");
      if (selected) selected.innerHTML = "";
    });
  }

  document.addEventListener("DOMContentLoaded", initExplore);
})();
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** ตรวจ spin/modal/loading ตรง DESIGN.md 14-15 + escape ทุกจุด render

### Step 6: เขียน tests/test_web.py + เติมเทส format/console (ผู้รับผิดชอบ: Khong, Debugger) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน test_web.py ด้วย Flask test client หน่อย mock run_roulette_simulation กับ get_meal_by_id เทส index/search สำเร็จ/search invalid/search error/detail/detail-404 รวม 6 เทส แล้วเติมเทส format 3 เคสใน test_engine กับแก้ test_main ให้ตรวจ formatted dict

**AI Response:**
AI ให้ test_web ทั้งไฟล์ + ส่วนที่เติมในอีก 2 ไฟล์ด้านล่าง

```python
# tests/test_web.py - ทั้งไฟล์
"""Unit tests for the Flask web application (src/web_app.py)."""

from unittest.mock import patch

import pytest

from src import web_app
from src.web_app import app

RAW_MEAL = {
    "idMeal": "52968",
    "strMeal": "Pork Souvlaki",
    "strCategory": "Pork",
    "strArea": "Greek",
    "strMealThumb": "http://img/pork-souvlaki.jpg",
    "strInstructions": "Mix pork with lemon and garlic.\nGrill and serve.",
    "strIngredient1": "pork",
    "strIngredient2": "garlic",
    "strIngredient3": "lemon",
}

FORMATTED = web_app.format_recipe(RAW_MEAL)


@pytest.fixture
def client():
    """Flask test client for the web application."""
    with app.test_client() as test_client:
        yield test_client


def test_index_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "fridge" in resp.get_data(as_text=True).lower()


@patch("src.web_app.run_roulette_simulation")
def test_api_search_success(mock_run, client):
    mock_run.return_value = {
        "status": "success",
        "query": ["pork", "garlic"],
        "match_count": 1,
        "selected_recipe": FORMATTED,
        "top_recipes": [FORMATTED],
    }
    resp = client.post("/api/search", json={"ingredients": "pork, garlic"})

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "success"
    assert data["match_count"] == 1
    assert data["top_recipes"][0]["name"] == "Pork Souvlaki"
    assert data["selected_recipe"]["ingredients"] == [
        "pork",
        "garlic",
        "lemon",
    ]
    mock_run.assert_called_once_with("pork, garlic")


@patch("src.web_app.run_roulette_simulation")
def test_api_search_invalid_input(mock_run, client):
    mock_run.return_value = {
        "status": "error",
        "message": "Ingredients must not contain numbers.",
    }
    resp = client.post("/api/search", json={"ingredients": "pork 123"})

    assert resp.status_code == 200
    assert resp.get_json()["status"] == "error"


@patch("src.web_app.run_roulette_simulation")
def test_api_search_api_error(mock_run, client):
    mock_run.return_value = {"status": "error", "message": "API failed"}
    resp = client.post("/api/search", json={"ingredients": "chicken"})

    assert resp.status_code == 200
    assert resp.get_json()["message"] == "API failed"


@patch("src.web_app.get_meal_by_id")
def test_recipe_detail(mock_get, client):
    mock_get.return_value = RAW_MEAL
    resp = client.get("/recipe/52968")

    assert resp.status_code == 200
    body = resp.get_json()
    assert body["name"] == "Pork Souvlaki"
    assert body["area"] == "Greek"
    assert body["ingredients"] == ["pork", "garlic", "lemon"]
    assert body["instructions"] == (
        "Mix pork with lemon and garlic.\nGrill and serve."
    )


@patch("src.web_app.get_meal_by_id")
def test_recipe_detail_not_found(mock_get, client):
    mock_get.return_value = None
    resp = client.get("/recipe/99999")
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Recipe not found"
```

```python
# tests/test_engine.py - เฉพาะส่วนที่เติม Sprint 3 (บรรทัด 192-235)
# --- format_recipe ---


def test_format_recipe_full():
    """All TheMealDB display fields are mapped to friendly keys."""
    meal = {
        "idMeal": "52772",
        "strMeal": "Teriyaki Chicken Casserole",
        "strCategory": "Chicken",
        "strArea": "Japanese",
        "strMealThumb": "http://img/1.jpg",
        "strInstructions": "Cook it.",
        "strYoutube": "http://y.tube/abc",
        "strIngredient1": "Soy Sauce",
        "strIngredient2": "",
    }

    result = format_recipe(meal)

    assert result["name"] == "Teriyaki Chicken Casserole"
    assert result["category"] == "Chicken"
    assert result["area"] == "Japanese"
    assert result["image_url"] == "http://img/1.jpg"
    assert result["instructions"] == "Cook it."
    assert result["youtube_url"] == "http://y.tube/abc"
    assert result["ingredients"] == ["soy sauce"]
    assert result["score"] is None


def test_format_recipe_keeps_score():
    """Ranked meals carry their score through formatting."""
    meal = {**MOCK_MEAL_52772, "score": 1.0}

    assert format_recipe(meal)["score"] == 1.0


def test_format_recipe_missing_fields():
    """Missing optional fields default to empty strings."""
    result = format_recipe({"idMeal": "1"})

    assert result["instructions"] == ""
    assert result["image_url"] == ""
    assert result["youtube_url"] == ""
    assert result["ingredients"] == []
```

```python
# tests/test_main.py - ทั้งไฟล์ (แก้ให้ตรวจ formatted dict + console)
"""Unit tests for src/main.py entry point logic."""

from unittest.mock import patch

from src.api_client import APIError
from src.main import run_console, run_roulette_simulation

MOCK_MEAL = {
    "idMeal": "52772",
    "strMeal": "Pork Souvlaki",
    "strCategory": "Pork",
    "strArea": "Greek",
    "strMealThumb": "http://img/pork.jpg",
    "strInstructions": "Grill and serve.",
    "strIngredient1": "pork",
    "strIngredient2": "lemon",
    "score": 1.0,
}
MOCK_RANKED = [MOCK_MEAL]


@patch("src.main.pick_random_recipe")
@patch("src.main.filter_and_rank")
def test_run_roulette_simulation_success(mock_rank, mock_pick):
    """Valid ingredients return a GUI-ready formatted result."""
    mock_rank.return_value = MOCK_RANKED
    mock_pick.return_value = MOCK_MEAL

    result = run_roulette_simulation("Pork, Garlic")

    assert result["status"] == "success"
    assert result["query"] == ["pork", "garlic"]
    assert result["match_count"] == 1

    selected = result["selected_recipe"]
    assert selected["name"] == "Pork Souvlaki"
    assert selected["ingredients"] == ["pork", "lemon"]
    assert selected["instructions"] == "Grill and serve."
    assert selected["image_url"] == "http://img/pork.jpg"
    assert selected["score"] == 1.0
    assert result["top_recipes"][0]["name"] == "Pork Souvlaki"


@patch("src.main.pick_random_recipe")
@patch("src.main.filter_and_rank")
def test_run_roulette_simulation_no_match(mock_rank, mock_pick):
    """Ingredients with no matching recipe return zero matches."""
    mock_rank.return_value = []
    mock_pick.return_value = None

    result = run_roulette_simulation("avocado, tofu")

    assert result["status"] == "success"
    assert result["match_count"] == 0
    assert result["selected_recipe"] is None
    assert result["top_recipes"] == []


@patch("src.main.filter_and_rank")
def test_run_roulette_simulation_api_error(mock_rank):
    """Live API failure surfaces as an error result."""
    mock_rank.side_effect = APIError("API failed")

    result = run_roulette_simulation("chicken")

    assert result["status"] == "error"
    assert result["message"] == "API failed"


def test_run_roulette_simulation_invalid_input():
    """Input containing numbers is rejected with an error result."""
    result = run_roulette_simulation("pork, egg123")

    assert result["status"] == "error"
    assert "numbers" in result["message"]


def test_run_roulette_simulation_empty_input():
    """Empty input is rejected with an error result."""
    result = run_roulette_simulation("")

    assert result["status"] == "error"


@patch("src.main.pick_random_recipe")
@patch("src.main.filter_and_rank")
def test_run_console(mock_rank, mock_pick, monkeypatch, capsys):
    """Interactive console session prints the execution result."""
    mock_rank.return_value = MOCK_RANKED
    mock_pick.return_value = MOCK_MEAL
    monkeypatch.setattr("builtins.input", lambda _prompt: "Pork, Garlic")

    run_console()

    captured = capsys.readouterr()
    assert "Execution Result:" in captured.out
    assert "selected_recipe" in captured.out
    assert "Pork Souvlaki" in captured.out
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** pytest รวมเขียว (รวม test_web 6 เทสใหม่)

### Step 7: requirements + deploy entry (ผู้รับผิดชอบ: ทีม) (เรียบเรียงใหม่)

**User Prompt:**
> เพิ่ม Flask ใน requirements หน่อย แล้วทำ entry ให้ Vercel เริ่มจากลอง vercel.json + api/index.py ก่อน ถ้าไม่เวิร์กค่อยใช้ src/app.py

**AI Response:**
AI เติม Flask>=3.0.0 แล้วทำ deploy 2 รอบตามประวัติ git โค้ดด้านล่าง

```text
# requirements.txt - ทั้งไฟล์ที่ HEAD
# Testing & Code Quality (Sprint 1)
pytest>=7.4.0
pytest-cov>=4.1.0
flake8>=6.1.0
black>=23.9.0

# API & Data Handling (สำหรับ Sprint 2 และ 3)
requests>=2.31.0

# Web App Framework (Sprint 3)
Flask>=3.0.0
```

หลักฐาน deploy (ไฟล์ชั่วคราว ถูกลบที่ 0dfb73b เหลือ src/app.py ใน Step 3):

```json
// vercel.json ที่ commit 6a3769d (ถูกลบที่ 0dfb73b)
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/api/index"
    }
  ]
}
```

```python
# api/index.py ที่ commit 6a3769d (ถูกลบที่ 0dfb73b)
"""Vercel entry point.

Exposes the Flask WSGI app from src/web_app.py as ``app`` so Vercel's
Python runtime can serve the entire application through a single function.
"""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SRC = _PROJECT_ROOT / "src"

for _path in (str(_PROJECT_ROOT), str(_SRC)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from web_app import app  # noqa: E402
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** commit 0dfb73b ตัด vercel.json/api ทิ้งใช้ src/app.py แทนตาม S3STAT

## ตารางสรุป

| ขั้นตอน | ไฟล์ | ผู้รับผิดชอบ | สิ่งที่ AI ช่วย | สิ่งที่ทีมทำเอง |
|---|---|---|---|---|
| 1 วางแผน | - (PLAN) | Benz | เสนอ thin layer + 3 routes | เขียน PLAN/DoD เอง |
| 2 format | engine (+19) + main | Toey | mapping + ผูก formatted dict | เติมเทส format |
| 3 web | web_app.py + app.py | Toey | routes + anchor + re-export | แก้ path 2 โหมด |
| 4 templates | base/index/results (142 บรรทัด) | Ter | layout ตาม DESIGN | ตรวจ responsive/modal |
| 5 static | style.css + app.js (629 บรรทัด) | Ter | theme + fetch/modal/spin | ตรวจ XSS escape |
| 6 tests | test_web + เติม engine/main | Khong | โค้ด mock + client | รันเขียว |
| 7 env/deploy | requirements + app/vercel/api | ทีม | เติม Flask + entry 2 แบบ | เลือก src/app.py |

---

[Back to top](#top) | [README](../README.md)
