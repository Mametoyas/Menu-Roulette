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
