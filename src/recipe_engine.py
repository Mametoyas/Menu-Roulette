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
