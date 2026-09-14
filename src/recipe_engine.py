"""Recipe search engine and mock dataset handling."""

import random
from typing import Dict, List, Optional

# Mock Data simulating TheMealDB API response structure[cite: 1, 3]
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


def filter_recipes_by_ingredients(
    user_ingredients: List[str], recipes: Optional[List[Dict]] = None
) -> List[Dict]:
    """
    Finds recipes containing at least one of the provided ingredients.
    """
    dataset = recipes if recipes is not None else MOCK_RECIPES
    matched = []

    for recipe in dataset:
        recipe_ingr = [ing.lower() for ing in recipe.get("ingredients", [])]
        # Check intersection between user query and recipe ingredients
        if any(ing in recipe_ingr for ing in user_ingredients):
            matched.append(recipe)

    return matched


def pick_random_recipe(matched_recipes: List[Dict]) -> Optional[Dict]:
    """Returns a random recipe from matched list, or None if list is empty."""
    if not matched_recipes:
        return None
    return random.choice(matched_recipes)
