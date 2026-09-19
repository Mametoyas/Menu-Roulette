# Sprint 2 — Tester Guide (เตอร์)

## หน้าที่
เขียน Unit Tests สำหรับ `api_client.py` และ `recipe_engine.py` โดยใช้ `unittest.mock` แทนการยิง API จริง และตั้งค่า CI/CD ผ่าน GitHub Actions

---

## สิ่งที่ต้องทำ

1. เขียน `tests/test_api.py` — test `api_client.py` ด้วย mock HTTP responses
2. เขียน `tests/test_engine.py` — test `recipe_engine.py` ด้วย mock API functions
3. สร้าง `.github/workflows/test.yml` — CI/CD รัน pytest อัตโนมัติ

---

## 1. `tests/test_api.py`

ทดสอบ `search_by_ingredient`, `get_meal_by_id`, `extract_ingredients` โดยไม่ยิง API จริง

```python
"""Unit tests for api_client.py using mocked HTTP responses."""

import pytest
from unittest.mock import patch, MagicMock
from src.api_client import (
    search_by_ingredient,
    get_meal_by_id,
    extract_ingredients,
    APIError,
)

MOCK_SEARCH_RESPONSE = {
    "meals": [
        {"idMeal": "52772", "strMeal": "Teriyaki Chicken Casserole", "strMealThumb": ""},
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
    import requests
    mock_get.side_effect = requests.exceptions.Timeout
    # TODO: ตรวจสอบว่า search_by_ingredient raise APIError เมื่อ timeout
    pass


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

---

## 2. `tests/test_engine.py`

ทดสอบ `search_recipes`, `score_recipe`, `filter_and_rank`, `pick_random_recipe` โดย mock `api_client` functions

```python
"""Unit tests for recipe_engine.py using mocked API functions."""

import pytest
from unittest.mock import patch

MOCK_MEALS = [
    {
        "idMeal": "52772",
        "strMeal": "Teriyaki Chicken Casserole",
        "strIngredient1": "chicken",
        "strIngredient2": "garlic",
        "strIngredient3": "soy sauce",
        "strIngredient4": "",
    },
    {
        "idMeal": "52907",
        "strMeal": "Egg Fried Rice",
        "strIngredient1": "egg",
        "strIngredient2": "garlic",
        "strIngredient3": "soy sauce",
        "strIngredient4": "",
    },
]


# --- score_recipe ---

def test_score_recipe_full_match():
    """Score = 1.0 when all user ingredients are in the recipe."""
    from src.recipe_engine import score_recipe
    score = score_recipe(MOCK_MEALS[0], ["chicken", "garlic"])
    assert score == 1.0


def test_score_recipe_partial_match():
    """Score = 0.5 when half of user ingredients match."""
    from src.recipe_engine import score_recipe
    score = score_recipe(MOCK_MEALS[0], ["chicken", "egg"])
    assert score == 0.5


def test_score_recipe_no_match():
    """Score = 0.0 when no user ingredients match."""
    from src.recipe_engine import score_recipe
    score = score_recipe(MOCK_MEALS[0], ["avocado", "mango"])
    assert score == 0.0


# --- search_recipes ---

@patch("src.recipe_engine.search_by_ingredient")
@patch("src.recipe_engine.get_meal_by_id")
def test_search_recipes_deduplication(mock_get_meal, mock_search):
    """Same meal ID from multiple ingredients is fetched only once."""
    from src.recipe_engine import search_recipes
    mock_search.return_value = [{"idMeal": "52772"}]
    mock_get_meal.return_value = MOCK_MEALS[0]

    result = search_recipes(["chicken", "garlic"])
    assert len(result) == 1
    mock_get_meal.assert_called_once_with("52772")


@patch("src.recipe_engine.search_by_ingredient")
@patch("src.recipe_engine.get_meal_by_id")
def test_search_recipes_empty(mock_get_meal, mock_search):
    """Returns empty list when API finds no meals."""
    from src.recipe_engine import search_recipes
    mock_search.return_value = []
    result = search_recipes(["avocado"])
    assert result == []


# --- filter_and_rank ---

@patch("src.recipe_engine.search_recipes")
def test_filter_and_rank_sorted(mock_search):
    """Recipes are sorted by score descending."""
    from src.recipe_engine import filter_and_rank
    mock_search.return_value = MOCK_MEALS
    result = filter_and_rank(["chicken", "garlic"])
    assert result[0]["score"] >= result[-1]["score"]


@patch("src.recipe_engine.search_recipes")
def test_filter_and_rank_min_score(mock_search):
    """Recipes below min_score are excluded."""
    from src.recipe_engine import filter_and_rank
    mock_search.return_value = MOCK_MEALS
    result = filter_and_rank(["chicken"], min_score=1.0)
    assert all(r["score"] >= 1.0 for r in result)


# --- pick_random_recipe ---

def test_pick_random_recipe_returns_top():
    """Returns a recipe from the top-scored group."""
    from src.recipe_engine import pick_random_recipe
    ranked = [
        {"idMeal": "1", "strMeal": "A", "score": 1.0},
        {"idMeal": "2", "strMeal": "B", "score": 1.0},
        {"idMeal": "3", "strMeal": "C", "score": 0.5},
    ]
    result = pick_random_recipe(ranked)
    assert result["score"] == 1.0


def test_pick_random_recipe_empty():
    """Returns None when list is empty."""
    from src.recipe_engine import pick_random_recipe
    assert pick_random_recipe([]) is None
```

---

## 3. `.github/workflows/test.yml`

สร้างไฟล์นี้เพื่อให้ GitHub Actions รัน pytest อัตโนมัติทุกครั้งที่มี push หรือ pull request

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

---

## รัน Tests

```bash
# รัน test ทั้งหมด
pytest -v

# รันเฉพาะ api tests
pytest tests/test_api.py -v

# รันเฉพาะ engine tests
pytest tests/test_engine.py -v

# รันพร้อม coverage report
pytest --cov=src -v
```
