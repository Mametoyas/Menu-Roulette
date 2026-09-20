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
