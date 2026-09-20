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