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
