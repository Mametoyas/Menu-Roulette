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