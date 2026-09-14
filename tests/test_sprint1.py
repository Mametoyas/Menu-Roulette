"""Automated unit tests for Sprint 1 logic validation."""

import pytest
from src.recipe_engine import (
    filter_recipes_by_ingredients,
    pick_random_recipe,
)
from src.utils import InvalidIngredientError, clean_ingredient_input


def test_clean_ingredient_input_valid():
    """Verify normalization of valid mixed case strings."""
    result = clean_ingredient_input(" Pork , Egg! , garlic ")
    assert result == ["pork", "egg", "garlic"]


def test_clean_ingredient_input_numeric_error():
    """Verify exception handling when numbers are passed."""
    with pytest.raises(InvalidIngredientError):
        clean_ingredient_input("pork, egg123")


def test_clean_ingredient_empty_error():
    """Verify exception on whitespace/empty inputs."""
    with pytest.raises(InvalidIngredientError):
        clean_ingredient_input("   ,  ")


def test_filter_recipes_success():
    """Verify correct recipe filtering logic."""
    matches = filter_recipes_by_ingredients(["pork"])
    assert len(matches) == 2
    assert all("pork" in r["ingredients"] for r in matches)


def test_filter_recipes_no_match():
    """Verify output when no ingredients match dataset."""
    matches = filter_recipes_by_ingredients(["avocado"])
    assert len(matches) == 0
    assert pick_random_recipe(matches) is None
