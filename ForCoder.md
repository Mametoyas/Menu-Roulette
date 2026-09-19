# Sprint 2 — Coder Guide

## โขง — `src/api_client.py`

### หน้าที่
เชื่อมต่อ TheMealDB API ดึงข้อมูล JSON และจัดการ error ต่างๆ

### สิ่งที่ต้องทำ
1. เขียนฟังก์ชัน `search_by_ingredient(ingredient)` — ค้นหา recipe IDs จาก ingredient
2. เขียนฟังก์ชัน `get_meal_by_id(meal_id)` — ดึงรายละเอียด recipe เต็มจาก ID
3. เขียนฟังก์ชัน `extract_ingredients(meal)` — แปลง JSON ของ TheMealDB ให้เป็น list ของ ingredients
4. จัดการ error: timeout, HTTP error, response ว่าง

### ตัวอย่างโค้ด

```python
"""TheMealDB API client for fetching recipe data."""

import requests
from typing import Optional

BASE_URL = "https://www.themealdb.com/api/json/v1/1"
TIMEOUT = 5


class APIError(Exception):
    """Raised when the API request fails."""
    pass


def search_by_ingredient(ingredient: str) -> list[dict]:
    """Returns a list of meals matching the given ingredient.

    Each item contains: idMeal, strMeal, strMealThumb
    """
    url = f"{BASE_URL}/filter.php"
    # TODO: ส่ง request ไปที่ url พร้อม params={"i": ingredient}
    # TODO: ถ้า status code ไม่ใช่ 200 ให้ raise APIError
    # TODO: ถ้า response["meals"] เป็น None ให้ return []
    # TODO: return response["meals"]
    pass


def get_meal_by_id(meal_id: str) -> Optional[dict]:
    """Returns full meal details for the given meal ID."""
    url = f"{BASE_URL}/lookup.php"
    # TODO: ส่ง request พร้อม params={"i": meal_id}
    # TODO: ถ้า meals เป็น None ให้ return None
    # TODO: return meals[0]
    pass


def extract_ingredients(meal: dict) -> list[str]:
    """Extracts ingredient list from a TheMealDB meal object.

    TheMealDB stores ingredients as strIngredient1..strIngredient20
    """
    ingredients = []
    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}", "")
        # TODO: ถ้า ingredient ไม่ว่างให้ append เข้า list (lowercase + strip)
    return ingredients
```

### ตัวอย่าง Response จาก TheMealDB
```json
{
  "meals": [
    {
      "idMeal": "52772",
      "strMeal": "Teriyaki Chicken Casserole",
      "strIngredient1": "chicken",
      "strIngredient2": "soy sauce",
      "strIngredient3": "garlic",
      "strIngredient4": "",
      ...
    }
  ]
}
```

---

## เบ็นซ์ — `src/recipe_engine.py`

### หน้าที่
อัปเกรด recipe_engine.py จาก mock data ให้ใช้ข้อมูลจาก API จริง พร้อม scoring, filtering และ random recommendation

### สิ่งที่ต้องทำ
1. เขียนฟังก์ชัน `search_recipes(ingredients)` — รวบรวม recipe IDs จากทุก ingredient แล้ว deduplicate
2. เขียนฟังก์ชัน `score_recipe(meal, user_ingredients)` — คำนวณ match score
3. อัปเกรด `filter_recipes_by_ingredients()` — ให้รับ meal objects จาก API แทน mock data
4. อัปเกรด `pick_random_recipe()` — ให้เลือกจาก top-scored recipes

### ตัวอย่างโค้ด

```python
"""Recipe search engine — Sprint 2 upgrade using live API data."""

import random
from typing import Optional
from api_client import search_by_ingredient, get_meal_by_id, extract_ingredients, APIError


def search_recipes(user_ingredients: list[str]) -> list[dict]:
    """Fetches and deduplicates recipes for all user ingredients.

    Returns a list of unique meal detail dicts from TheMealDB.
    """
    seen_ids = set()
    meals = []

    for ingredient in user_ingredients:
        # TODO: เรียก search_by_ingredient(ingredient)
        # TODO: วน loop ผ่าน results แต่ละตัว
        # TODO: ถ้า idMeal ยังไม่อยู่ใน seen_ids ให้เรียก get_meal_by_id()
        # TODO: เพิ่ม meal เข้า meals และ id เข้า seen_ids
        pass

    return meals


def score_recipe(meal: dict, user_ingredients: list[str]) -> float:
    """Calculates ingredient match score.

    Score = Matched User Ingredients / Total User Ingredients
    """
    recipe_ingredients = extract_ingredients(meal)
    # TODO: นับจำนวน user_ingredients ที่อยู่ใน recipe_ingredients
    # TODO: return matched / len(user_ingredients)
    pass


def filter_and_rank(
    user_ingredients: list[str],
    min_score: float = 0.0
) -> list[dict]:
    """Returns recipes sorted by score (descending), filtered by min_score."""
    meals = search_recipes(user_ingredients)

    scored = []
    for meal in meals:
        score = score_recipe(meal, user_ingredients)
        if score >= min_score:
            # TODO: เพิ่ม key "score" เข้าไปใน meal dict
            scored.append(meal)

    # TODO: sort scored by "score" descending
    return scored


def pick_random_recipe(ranked_recipes: list[dict]) -> Optional[dict]:
    """Randomly selects from the top-scored recipes."""
    if not ranked_recipes:
        return None

    top_score = ranked_recipes[0]["score"]
    # TODO: filter เฉพาะ recipes ที่มี score == top_score
    # TODO: return random.choice จาก top candidates
    pass
```

---

## การทดสอบ

โขงและเบ็นซ์ควร run ทดสอบด้วย:

```bash
pytest tests/test_api.py -v
pytest tests/test_engine.py -v
```

หรือรันทั้งหมด:

```bash
pytest -v
```
