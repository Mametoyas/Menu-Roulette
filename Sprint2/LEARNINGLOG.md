<a id="top"></a>

[README](../README.md) | [Members](../MEMBERS.md) | [Plan](../PLAN.md) | [Design](../DESIGN.md) | [Sprint1](../Sprint1/README.md) | [Sprint2](../Sprint2/README.md) | [Sprint3](../Sprint3/README.md) | [Changelog](../CHANGELOG.md) | [Review](../SPRINT_REVIEW.md) | [Peer Eval](../PEER_EVALUATION.md) | [AI Log S1](../Sprint1/LEARNINGLOG.md)

# ประวัติการใช้ AI - Sprint 2 (AI Usage Log)

โปรเจกต์: Recipe Roulette (TheMealDB) | ช่วงงาน: 19-20/09/2569 (ส่ง 25/09/2569) | ทีม: Toey (Planner) / Khong (Coder api_client) / Benz (Coder engine) / Ter (Debugger+CI)

## หมายเหตุด้านความถูกต้อง

- โค้ดตรงกับไฟล์ที่ commit 5809544 (fix main.py by Planner) ทุกตัวอักษร ดึงด้วย git show ตรง
- บทสนทนา User Prompt เรียบเรียงใหม่จากหลักฐานในไฟล์ + PLAN.md + Sprint2.md ทุก Step ติดป้าย (เรียบเรียงใหม่)
- บทบาทอ้างอิง PLAN.md ช่วง Sprint 2: เต้ย Planner, โขง Coder api_client, เบ็นซ์ Coder engine, เตอร์ Debugger/CI

### Step 1: วางแผน Sprint 2 + Kanban (ผู้รับผิดชอบ: Toey, Planner) (เรียบเรียงใหม่)

**User Prompt:**
> ช่วยวาง Sprint 2 หน่อย จะย้ายจาก Mock ไปต่อ TheMealDB API จริง มี scoring/filter/rank/sุ่มตัวท็อป ทำ CI ด้วย GitHub Actions แบ่งงาน Khong (api_client) Benz (engine) Ter (test+CI) ขอ DoD ที่ตรวจได้

**AI Response:**
AI เสนอ BLL/DAL แยกชั้น สูตร Score = matched/total, dedup ด้วย idMeal, mock HTTP ในเทส, CI รัน pytest บน main/develop ทีมนำไปเขียน PLAN.md ช่วง Sprint 2 และตั้ง Kanban เอง

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** Planner จัด Kanban + branching strategy เอง (ตาม PLAN.md)

### Step 2: เขียน src/api_client.py (ผู้รับผิดชอบ: Khong, Coder) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน src/api_client.py ต่อ TheMealDB (BASE_URL อ่านจาก env MEALDB_BASE_URL มี default, TIMEOUT 5) มี search_by_ingredient (filter.php?i=) คืน [] เมื่อ meals null, get_meal_by_id (lookup.php) คืน None เมื่อไม่เจอ, extract_ingredients ไล่ strIngredient1..20 ตัดว่าง+lower, error ทั้งหมดเป็น APIError (ห่อ RequestException + status != 200)

**AI Response:**
AI อธิบาย 3 ฟังก์ชัน + คลาส APIError พร้อมโค้ดด้านล่าง

```python
"""TheMealDB API client for fetching recipe data."""

import os
from typing import Optional
import requests

BASE_URL = os.getenv(
    "MEALDB_BASE_URL", "https://www.themealdb.com/api/json/v1/1"
)
TIMEOUT = 5


class APIError(Exception):
    """Raised when the API request fails."""
    pass


def search_by_ingredient(ingredient: str) -> list[dict]:
    """Returns a list of meals matching the given ingredient.

    Each item contains: idMeal, strMeal, strMealThumb
    """
    url = f"{BASE_URL}/filter.php"
    try:
        response = requests.get(url, params={"i": ingredient}, timeout=TIMEOUT)
        if response.status_code != 200:
            raise APIError(
                f"API request failed with status code {response.status_code}"
            )
        data = response.json()
        meals = data.get("meals")
        if meals is None:
            return []
        return meals
    except requests.exceptions.RequestException as e:
        raise APIError(
            f"Error fetching meals for ingredient '{ingredient}': {e}"
        ) from e


def get_meal_by_id(meal_id: str) -> Optional[dict]:
    """Returns full meal details for the given meal ID."""
    url = f"{BASE_URL}/lookup.php"
    try:
        response = requests.get(url, params={"i": meal_id}, timeout=TIMEOUT)
        if response.status_code != 200:
            raise APIError(
                f"API request failed with status code {response.status_code}"
            )
        data = response.json()
        meals = data.get("meals")
        if not meals:
            return None
        return meals[0]
    except requests.exceptions.RequestException as e:
        raise APIError(
            f"Error fetching meal with ID '{meal_id}': {e}"
        ) from e


def extract_ingredients(meal: dict) -> list[str]:
    """Extracts ingredient list from a TheMealDB meal object.

    TheMealDB stores ingredients as strIngredient1..strIngredient20
    """
    ingredients = []
    for i in range(1, 21):
        raw_ingredient = meal.get(f"strIngredient{i}")
        if raw_ingredient and isinstance(raw_ingredient, str):
            cleaned = raw_ingredient.strip().lower()
            if cleaned:
                ingredients.append(cleaned)
    return ingredients
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** เทสด้วย unittest.mock ไม่ยิงเน็ตจริง (ดู Step 5), ตั้ง BASE_URL default เป็น public API ไม่ต้องใช้ key

### Step 3: อัปเกรด src/recipe_engine.py ใช้ live API (ผู้รับผิดชอบ: Benz, Coder) (เรียบเรียงใหม่)

**User Prompt:**
> อัปเกรด recipe_engine.py จาก Mock ไปใช้ live API หน่อย เพิ่ม search_recipes (ยิงต่อวัตถุดิบ dedup ด้วย idMeal ข้ามอันที่ lookup ไม่เจอ), score_recipe (matched/total กันหารศูนย์), filter_and_rank (ติด score ไม่ mutate input เรียงมากไปน้อย), pick_random_recipe (สุ่มเฉพาะกลุ่มคะแนนสูงสุด ถ้าไม่มี score ใช้วิธีเดิม) คง filter_recipes_by_ingredients + MOCK ไว้ให้ Sprint 1 ทำงานออฟไลน์ได้ รองรับรันทั้ง python src/main.py และ pytest

**AI Response:**
AI อธิบาย search/dedup/score/rank/top-pick พร้อมชั้น _recipe_ingredients รองรับทั้ง mock (ingredients) และ live (strIngredient) โค้ดด้านล่าง (ยังไม่มี format_recipe ซึ่งเกิด Sprint 3 commit 38657d1)

```python
"""Recipe search engine — Sprint 2 upgrade using live API data."""

import random
from typing import Dict, List, Optional

# Import supports both execution modes:
#   python src/main.py      -> api_client (src/ on sys.path)
#   pytest (pythonpath = .) -> src.api_client
try:
    from api_client import (
        search_by_ingredient,
        get_meal_by_id,
        extract_ingredients,
    )
except ImportError:
    from src.api_client import (
        search_by_ingredient,
        get_meal_by_id,
        extract_ingredients,
    )


# Mock Data simulating TheMealDB API response structure (Sprint 1)
MOCK_RECIPES: List[Dict] = [
    {
        "idMeal": "52772",
        "strMeal": "Teriyaki Chicken Casserole",
        "strCategory": "Chicken",
        "ingredients": ["chicken", "rice", "soy sauce", "egg"],
    },
    {
        "idMeal": "52968",
        "strMeal": "Pork Souvlaki",
        "strCategory": "Pork",
        "ingredients": ["pork", "lemon", "olive oil", "garlic"],
    },
    {
        "idMeal": "52855",
        "strMeal": "Banana Pancakes",
        "strCategory": "Dessert",
        "ingredients": ["banana", "egg", "flour", "milk"],
    },
    {
        "idMeal": "52907",
        "strMeal": "Egg Fried Rice",
        "strCategory": "Vegetarian",
        "ingredients": ["rice", "egg", "garlic", "soy sauce"],
    },
    {
        "idMeal": "53013",
        "strMeal": "Garlic Butter Pork Chop",
        "strCategory": "Pork",
        "ingredients": ["pork", "garlic", "butter"],
    },
]


def _recipe_ingredients(recipe: Dict) -> List[str]:
    """Returns a lowercase ingredient list from an API meal or mock dict.

    API meal objects store ingredients as strIngredient1..strIngredient20,
    while the mock dataset uses an "ingredients" key.
    """
    if "ingredients" in recipe:
        return [ing.lower() for ing in recipe.get("ingredients", [])]
    return extract_ingredients(recipe)


def search_recipes(user_ingredients: List[str]) -> List[Dict]:
    """Fetches and deduplicates recipes for all user ingredients.

    For each ingredient, queries TheMealDB, removes duplicate meal IDs,
    and fetches the full meal details.

    Args:
        user_ingredients: Cleaned ingredient names (lowercase).

    Returns:
        A list of unique meal detail dicts from TheMealDB.

    Raises:
        APIError: If a TheMealDB request fails.
    """
    seen_ids = set()
    meals: List[Dict] = []

    for ingredient in user_ingredients:
        results = search_by_ingredient(ingredient)
        for meal in results:
            meal_id = meal.get("idMeal")
            if meal_id and meal_id not in seen_ids:
                details = get_meal_by_id(meal_id)
                if details:
                    seen_ids.add(meal_id)
                    meals.append(details)

    return meals


def score_recipe(meal: Dict, user_ingredients: List[str]) -> float:
    """Calculates ingredient match score.

    Score = Matched User Ingredients / Total User Ingredients
    """
    if not user_ingredients:
        return 0.0

    recipe_ingredients = extract_ingredients(meal)
    matched = sum(1 for ing in user_ingredients if ing in recipe_ingredients)
    return matched / len(user_ingredients)


def filter_recipes_by_ingredients(
    user_ingredients: List[str], recipes: Optional[List[Dict]] = None
) -> List[Dict]:
    """Finds recipes containing at least one of the provided ingredients.

    Accepts meal dicts from TheMealDB (strIngredient1..20) or the mock
    dataset ("ingredients" key). Defaults to the mock dataset so Sprint 1
    behaviour keeps working offline.
    """
    dataset = recipes if recipes is not None else MOCK_RECIPES
    matched = []

    for recipe in dataset:
        recipe_ingr = _recipe_ingredients(recipe)
        if any(ing in recipe_ingr for ing in user_ingredients):
            matched.append(recipe)

    return matched


def filter_and_rank(
    user_ingredients: List[str], min_score: float = 0.0
) -> List[Dict]:
    """Returns live API recipes, scored and sorted descending by score.

    Only recipes with score >= min_score are included. Each returned dict
    carries a "score" key; the input meal dicts are not mutated.
    """
    meals = search_recipes(user_ingredients)

    scored = []
    for meal in meals:
        score = score_recipe(meal, user_ingredients)
        if score >= min_score:
            scored_meal = dict(meal)
            scored_meal["score"] = score
            scored.append(scored_meal)

    scored.sort(key=lambda m: m["score"], reverse=True)
    return scored


def pick_random_recipe(ranked_recipes: List[Dict]) -> Optional[Dict]:
    """Randomly selects from the top-scored recipes.

    If the recipes carry a "score" key (Sprint 2 flow), only the highest
    scoring candidates are considered. Falls back to a plain random choice
    for legacy/mock data without scores.
    """
    if not ranked_recipes:
        return None

    if "score" in ranked_recipes[0]:
        top_score = max(recipe["score"] for recipe in ranked_recipes)
        top_candidates = [
            recipe
            for recipe in ranked_recipes
            if recipe["score"] == top_score
        ]
        return random.choice(top_candidates)

    return random.choice(ranked_recipes)
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** เจอ Whoops ว่า mock ใช้ key ingredients แต่ live ใช้ strIngredient1..20 จึงเพิ่ม _recipe_ingredients (ดู Step 7)

### Step 4: อัปเกรด src/main.py เป็น live flow (ผู้รับผิดชอบ: ทีม Coder - commit แก้โดย Planner 5809544) (เรียบเรียงใหม่)

**User Prompt:**
> อัป main.py เป็น live API flow หน่อย pipeline Clean -> filter_and_rank -> pick_random_recipe จับ InvalidIngredientError กับ APIError แยกกัน แยก run_console (input/print) กับ if __name__ == main ให้รองรับทั้งรันตรงและ pytest

**AI Response:**
AI อธิบาย live pipeline + dual-import (utils ตรง / src.utils ใต้ pytest) พร้อมโค้ดด้านล่าง

```python
"""Console entry point — Sprint 2 live TheMealDB API flow."""

# Import supports both execution modes:
#   python src/main.py      -> utils / recipe_engine / api_client (src/ on sys.path)
#   pytest (pythonpath = .) -> src.utils / src.recipe_engine / src.api_client
try:  # pragma: no cover - exercised when running `python src/main.py`
    from utils import clean_ingredient_input, InvalidIngredientError
    from recipe_engine import filter_and_rank, pick_random_recipe
    from api_client import APIError
except ImportError:
    from src.utils import clean_ingredient_input, InvalidIngredientError
    from src.recipe_engine import filter_and_rank, pick_random_recipe
    from src.api_client import APIError


def run_roulette_simulation(raw_input: str) -> dict:
    """Executes the pipeline: Clean -> Live API Search/Score/Rank -> Random Pick."""
    try:
        cleaned_ingredients = clean_ingredient_input(raw_input)
        ranked = filter_and_rank(cleaned_ingredients)
        selected = pick_random_recipe(ranked)

        return {
            "status": "success",
            "query": cleaned_ingredients,
            "match_count": len(ranked),
            "selected_recipe": selected,
        }
    except InvalidIngredientError as e:
        return {"status": "error", "message": str(e)}
    except APIError as e:
        return {"status": "error", "message": str(e)}


def run_console() -> None:
    """Runs the interactive input()/print() roulette session."""
    sample_query = input("Enter the ingredients (example: 'Pork, Garlic'):")
    result = run_roulette_simulation(sample_query)
    print("Execution Result:", result)


if __name__ == "__main__":  # pragma: no cover
    run_console()
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** Planner แก้ main.py ปิดท้าย Sprint (commit 5809544 fix main.py by Planner)

### Step 5: เขียน tests/test_api.py (ผู้รับผิดชอบ: Ter, Debugger) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน tests/test_api.py ด้วย unittest.mock หน่อย mock requests.get ทั้งหมด เทส search (เจอ/ไม่เจอ/500/timeout), lookup (เจอ/ไม่เจอ/500/timeout), extract (ครบ/ข้ามค่าว่าง) รวม 10 เทส

**AI Response:**
AI อธิบาย helper make_mock_response + patch ปลายทาง src.api_client.requests.get พร้อมโค้ดด้านล่าง

```python
"""Unit tests for api_client.py using mocked HTTP responses."""

from unittest.mock import patch, MagicMock
import pytest
import requests
from src.api_client import (
    search_by_ingredient,
    get_meal_by_id,
    extract_ingredients,
    APIError,
)

MOCK_SEARCH_RESPONSE = {
    "meals": [
        {
            "idMeal": "52772",
            "strMeal": "Teriyaki Chicken Casserole",
            "strMealThumb": "",
        },
        {"idMeal": "52968", "strMeal": "Pork Souvlaki", "strMealThumb": ""},
    ]
}

MOCK_MEAL_DETAIL = {
    "meals": [
        {
            "idMeal": "52772",
            "strMeal": "Teriyaki Chicken Casserole",
            "strIngredient1": "chicken",
            "strIngredient2": "soy sauce",
            "strIngredient3": "garlic",
            "strIngredient4": "",
            # strIngredient5..20 จะเป็น "" หรือ None
        }
    ]
}


def make_mock_response(json_data: dict, status_code: int = 200) -> MagicMock:
    """Helper: สร้าง mock response object."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data
    return mock_resp


# --- search_by_ingredient ---

@patch("src.api_client.requests.get")
def test_search_by_ingredient_success(mock_get):
    """Returns list of meals when API responds with results."""
    mock_get.return_value = make_mock_response(MOCK_SEARCH_RESPONSE)
    result = search_by_ingredient("chicken")
    assert len(result) == 2
    assert result[0]["idMeal"] == "52772"


@patch("src.api_client.requests.get")
def test_search_by_ingredient_no_results(mock_get):
    """Returns empty list when API returns meals: null."""
    mock_get.return_value = make_mock_response({"meals": None})
    result = search_by_ingredient("avocado")
    assert result == []


@patch("src.api_client.requests.get")
def test_search_by_ingredient_api_error(mock_get):
    """Raises APIError on non-200 status code."""
    mock_get.return_value = make_mock_response({}, status_code=500)
    with pytest.raises(APIError):
        search_by_ingredient("chicken")


@patch("src.api_client.requests.get")
def test_search_by_ingredient_timeout(mock_get):
    """Raises APIError on request timeout."""
    mock_get.side_effect = requests.exceptions.Timeout
    with pytest.raises(APIError):
        search_by_ingredient("chicken")


# --- get_meal_by_id ---

@patch("src.api_client.requests.get")
def test_get_meal_by_id_success(mock_get):
    """Returns meal dict when ID is valid."""
    mock_get.return_value = make_mock_response(MOCK_MEAL_DETAIL)
    result = get_meal_by_id("52772")
    assert result["idMeal"] == "52772"
    assert result["strMeal"] == "Teriyaki Chicken Casserole"


@patch("src.api_client.requests.get")
def test_get_meal_by_id_not_found(mock_get):
    """Returns None when meal ID does not exist."""
    mock_get.return_value = make_mock_response({"meals": None})
    result = get_meal_by_id("99999")
    assert result is None


@patch("src.api_client.requests.get")
def test_get_meal_by_id_api_error(mock_get):
    """Raises APIError on non-200 status code."""
    mock_get.return_value = make_mock_response({}, status_code=500)
    with pytest.raises(APIError):
        get_meal_by_id("52772")


@patch("src.api_client.requests.get")
def test_get_meal_by_id_timeout(mock_get):
    """Raises APIError on request timeout."""
    mock_get.side_effect = requests.exceptions.Timeout
    with pytest.raises(APIError):
        get_meal_by_id("52772")


# --- extract_ingredients ---

def test_extract_ingredients_success():
    """Extracts non-empty ingredients from meal dict."""
    meal = MOCK_MEAL_DETAIL["meals"][0]
    result = extract_ingredients(meal)
    assert "chicken" in result
    assert "soy sauce" in result
    assert "garlic" in result


def test_extract_ingredients_skips_empty():
    """Does not include empty strIngredient fields."""
    meal = MOCK_MEAL_DETAIL["meals"][0]
    result = extract_ingredients(meal)
    assert "" not in result
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** ไม่ยิงเน็ตจริงเลย เทส deterministic (ตาม Sprint2.md Wow!)

### Step 6: เขียน tests/test_engine.py + tests/test_main.py (ผู้รับผิดชอบ: Ter, Debugger) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน test_engine.py (mock search_recipes เทส dedup/empty/skip-missing/error, score เต็ม/ครึ่ง/ศูนย์/หารศูนย์, rank sort/min-score/no-mutate/empty, pick top/empty/legacy, filter API meals) กับ test_main.py (mock rank/pick เทส success/no-match/api-error/invalid/empty/console) ให้หน่อย

**AI Response:**
AI ให้ 2 ไฟล์ด้านล่าง (test_engine 16 เทส ยังไม่มีกลุ่ม format_recipe ซึ่งเกิด Sprint 3)

```python
# tests/test_engine.py
"""Unit tests for recipe_engine.py — Sprint 2 API-based logic."""

from unittest.mock import patch

import pytest

from src.api_client import APIError
from src.recipe_engine import (
    filter_and_rank,
    filter_recipes_by_ingredients,
    pick_random_recipe,
    score_recipe,
    search_recipes,
)

# --- Fixture data (mimics TheMealDB response structure) ---

MOCK_SEARCH_RESULTS = [
    {"idMeal": "52772", "strMeal": "Teriyaki Chicken Casserole"},
    {"idMeal": "52968", "strMeal": "Pork Souvlaki"},
]

MOCK_MEAL_52772 = {
    "idMeal": "52772",
    "strMeal": "Teriyaki Chicken Casserole",
    "strIngredient1": "chicken",
    "strIngredient2": "rice",
    "strIngredient3": "soy sauce",
    "strIngredient4": "egg",
    "strIngredient5": "",
}

MOCK_MEAL_52968 = {
    "idMeal": "52968",
    "strMeal": "Pork Souvlaki",
    "strIngredient1": "pork",
    "strIngredient2": "lemon",
    "strIngredient3": "garlic",
    "strIngredient4": "",
}

MOCK_MEALS = {
    "52772": MOCK_MEAL_52772,
    "52968": MOCK_MEAL_52968,
}


# --- search_recipes ---


@patch("src.recipe_engine.get_meal_by_id")
@patch("src.recipe_engine.search_by_ingredient")
def test_search_recipes_deduplicates_and_fetches_details(
    mock_search, mock_get_meal
):
    """Returns unique meals even when the same meal matches 2 ingredients."""
    mock_search.side_effect = [MOCK_SEARCH_RESULTS, MOCK_SEARCH_RESULTS]
    mock_get_meal.side_effect = lambda meal_id: MOCK_MEALS[meal_id]

    meals = search_recipes(["chicken", "pork"])

    assert len(meals) == 2
    assert mock_get_meal.call_count == 2
    assert {m["idMeal"] for m in meals} == {"52772", "52968"}


@patch("src.recipe_engine.search_by_ingredient")
def test_search_recipes_empty_ingredients(mock_search):
    """Empty inputs return an empty list without hitting the API."""
    assert search_recipes([]) == []
    mock_search.assert_not_called()


@patch("src.recipe_engine.get_meal_by_id")
@patch("src.recipe_engine.search_by_ingredient")
def test_search_recipes_skips_missing_details(mock_search, mock_get_meal):
    """Meals without retrievable details are skipped."""
    mock_search.return_value = [{"idMeal": "99999"}]
    mock_get_meal.return_value = None

    assert search_recipes(["avocado"]) == []


@patch("src.recipe_engine.search_by_ingredient")
def test_search_recipes_api_error_propagates(mock_search):
    """API failures surface as APIError."""
    mock_search.side_effect = APIError("boom")

    with pytest.raises(APIError):
        search_recipes(["chicken"])


# --- score_recipe ---


def test_score_recipe_full_match():
    """All user ingredients are in the recipe -> score 1.0."""
    assert score_recipe(MOCK_MEAL_52772, ["chicken", "rice"]) == 1.0


def test_score_recipe_partial_match():
    """Half of the user ingredients match -> score 0.5."""
    assert score_recipe(MOCK_MEAL_52772, ["chicken", "pork"]) == 0.5


def test_score_recipe_no_match():
    """No user ingredients match -> score 0.0."""
    assert score_recipe(MOCK_MEAL_52772, ["avocado"]) == 0.0


def test_score_recipe_empty_user_ingredients():
    """Empty user ingredient list does not divide by zero."""
    assert score_recipe(MOCK_MEAL_52772, []) == 0.0


# --- filter_and_rank ---


@patch("src.recipe_engine.search_recipes")
def test_filter_and_rank_scores_and_sorts(mock_search):
    """Recipes are scored and sorted descending."""
    mock_search.return_value = [MOCK_MEAL_52968, MOCK_MEAL_52772]

    ranked = filter_and_rank(["chicken", "rice"])

    assert len(ranked) == 2
    assert "score" in ranked[0]
    scores = [recipe["score"] for recipe in ranked]
    assert scores == sorted(scores, reverse=True)


@patch("src.recipe_engine.search_recipes")
def test_filter_and_rank_respects_min_score(mock_search):
    """Recipes below min_score are excluded."""
    mock_search.return_value = [MOCK_MEAL_52772, MOCK_MEAL_52968]

    # Neither meal contains ALL of chicken+rice+pork -> all below 1.0
    ranked = filter_and_rank(["chicken", "rice", "pork"], min_score=1.0)

    assert ranked == []


@patch("src.recipe_engine.search_recipes")
def test_filter_and_rank_does_not_mutate_input(mock_search):
    """Passed-in meal dicts do not gain a score key."""
    meals = [dict(MOCK_MEAL_52772), dict(MOCK_MEAL_52968)]
    mock_search.return_value = meals

    filter_and_rank(["pork"])

    assert all("score" not in meal for meal in meals)


@patch("src.recipe_engine.search_recipes")
def test_filter_and_rank_no_results(mock_search):
    """No API results -> empty ranked list."""
    mock_search.return_value = []

    assert filter_and_rank(["avocado"]) == []


# --- pick_random_recipe ---


def test_pick_random_recipe_empty():
    """Empty list returns None."""
    assert pick_random_recipe([]) is None


def test_pick_random_recipe_picks_top_score():
    """Only the highest-scoring recipes are candidates."""
    recipes = [
        {"idMeal": "1", "score": 0.5},
        {"idMeal": "2", "score": 1.0},
        {"idMeal": "3", "score": 1.0},
    ]

    picked = pick_random_recipe(recipes)

    assert picked["score"] == 1.0
    assert picked["idMeal"] in {"2", "3"}


def test_pick_random_recipe_fallback_without_score():
    """Legacy/mock data without scores uses a plain random choice."""
    picked = pick_random_recipe([MOCK_MEAL_52772])

    assert picked["idMeal"] == "52772"


# --- filter_recipes_by_ingredients (API meal objects) ---


def test_filter_recipes_by_ingredients_api_meals():
    """Works with TheMealDB-style meal objects (strIngredient fields)."""
    meals = [MOCK_MEAL_52772, MOCK_MEAL_52968]

    matched = filter_recipes_by_ingredients(["pork"], recipes=meals)

    assert len(matched) == 1
    assert matched[0]["idMeal"] == "52968"


def test_filter_recipes_by_ingredients_no_match():
    """No matching ingredient -> empty list."""
    assert (
        filter_recipes_by_ingredients(["avocado"], recipes=[MOCK_MEAL_52772])
        == []
    )
```

```python
# tests/test_main.py
"""Unit tests for src/main.py entry point logic."""

from unittest.mock import patch

from src.api_client import APIError
from src.main import run_console, run_roulette_simulation

MOCK_RANKED = [{"idMeal": "52772", "strMeal": "Pork Souvlaki", "score": 1.0}]


@patch("src.main.pick_random_recipe")
@patch("src.main.filter_and_rank")
def test_run_roulette_simulation_success(mock_rank, mock_pick):
    """Valid ingredients return a success result with a selection."""
    mock_rank.return_value = MOCK_RANKED
    mock_pick.return_value = MOCK_RANKED[0]

    result = run_roulette_simulation("Pork, Garlic")

    assert result["status"] == "success"
    assert result["query"] == ["pork", "garlic"]
    assert result["match_count"] == 1
    assert result["selected_recipe"] is not None


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
    mock_pick.return_value = MOCK_RANKED[0]
    monkeypatch.setattr("builtins.input", lambda _prompt: "Pork, Garlic")

    run_console()

    captured = capsys.readouterr()
    assert "Execution Result:" in captured.out
    assert "status" in captured.out
```

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** รวมกับ test_sprint1 ที่เติม 2 เคส (empty string / whitespace only) ไฟล์ที่ฝังรวม 40 เทส (10+17+6+7) ส่วน Sprint2.md รายงาน 39 เทส (10+19+6+4) ตัวเลขเอกสารกับโค้ดคลาดกันเล็กน้อย ยึดไฟล์จริงเป็นหลัก

### Step 7: ตั้ง CI (.github/workflows/test.yml) + แก้ Whoops normalizer (ผู้รับผิดชอบ: Ter Debugger + Benz Coder) (เรียบเรียงใหม่)

**User Prompt:**
> เขียน .github/workflows/test.yml ให้หน่อย push/PR ไป main/develop รัน pytest -v บน Ubuntu Python 3.11 ตาม requirements.txt

**AI Response:**
AI ให้ workflow 4 step (checkout / setup-python 3.11 / pip install / pytest -v) โค้ดด้านล่าง

```yaml
name: Run Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest -v
```

**User Prompt (bugfix):**
> เทสพัง: mock ใช้ key ingredients แต่ live API ใช้ strIngredient1..20 ช่วยทำชั้นแปลงให้ filter รองรับทั้งสองแบบ

**AI Response:**
AI เพิ่ม _recipe_ingredients (มี ingredients ใช้ตรง ไม่มีเรียก extract_ingredients) ซึ่งอยู่ในโค้ด Step 3 แล้ว

**สิ่งที่ทีมตรวจสอบ/ปรับเอง:** บันทึก Whoops ใน Sprint2.md + เพิ่มเทส test_filter_recipes_by_ingredients_api_meals

### Step 8: requirements.txt (ยืนยัน - ไม่ต้องขอใหม่)

Sprint 2 ไม่เพิ่ม dependency ใหม่ ใช้ requirements เดิมจาก Sprint 1 (มี requests>=2.31.0 เผื่อไว้แล้วตั้งแต่ commit แรก) โค้ดด้านล่างตรงไฟล์ที่ 5809544

```text
# Testing & Code Quality (Sprint 1)
pytest>=7.4.0
pytest-cov>=4.1.0
flake8>=6.1.0
black>=23.9.0

# API & Data Handling (สำหรับ Sprint 2 และ 3)
requests>=2.31.0
```

## ตารางสรุป

| ขั้นตอน | ไฟล์ | ผู้รับผิดชอบ | สิ่งที่ AI ช่วย | สิ่งที่ทีมทำเอง |
|---|---|---|---|---|
| 1 วางแผน | - (PLAN/Kanban) | Toey | เสนอ BLL/DAL + สูตร score + CI | เขียน PLAN + Kanban เอง |
| 2 API client | src/api_client.py | Khong | โค้ด 3 ฟังก์ชัน + APIError | mock test + ตั้ง default URL |
| 3 engine | src/recipe_engine.py | Benz | search/score/rank/pick + dual-mode | เพิ่ม normalizer (Step 7) |
| 4 pipeline | src/main.py | ทีม Coder (Planner แก้ปิด) | live pipeline + dual-import | Planner แก้ main (5809544) |
| 5-6 tests | test_api/engine/main (+sprint1 2 เคส) | Ter | โค้ดเทส mock ทั้งหมด | รันเขียว + รายงาน QA |
| 7 CI+fix | test.yml + normalizer | Ter+Benz | workflow + ชี้สาเหตุ key ต่าง | เปิด CI + บันทึก Whoops |
| 8 env | requirements.txt | ทีม | ไม่ต้องเพิ่ม (มี requests แล้ว) | ยืนยัน pip install |

---

[Back to top](#top) | [README](../README.md)
