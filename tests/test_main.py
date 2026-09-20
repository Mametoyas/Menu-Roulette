"""Unit tests for src/main.py entry point logic."""

from src.main import run_console, run_roulette_simulation


def test_run_roulette_simulation_success():
    """Valid ingredients return a success result with a selection."""
    result = run_roulette_simulation("Pork, Garlic")

    assert result["status"] == "success"
    assert result["query"] == ["pork", "garlic"]
    assert result["match_count"] >= 1
    assert result["selected_recipe"] is not None


def test_run_roulette_simulation_no_match():
    """Ingredients with no matching recipe return zero matches."""
    result = run_roulette_simulation("avocado, tofu")

    assert result["status"] == "success"
    assert result["match_count"] == 0
    assert result["selected_recipe"] is None


def test_run_roulette_simulation_invalid_input():
    """Input containing numbers is rejected with an error result."""
    result = run_roulette_simulation("pork, egg123")

    assert result["status"] == "error"
    assert "numbers" in result["message"]


def test_run_roulette_simulation_empty_input():
    """Empty input is rejected with an error result."""
    result = run_roulette_simulation("")

    assert result["status"] == "error"


def test_run_console(monkeypatch, capsys):
    """Interactive console session prints the execution result."""
    monkeypatch.setattr("builtins.input", lambda _prompt: "Pork, Garlic")

    run_console()

    captured = capsys.readouterr()
    assert "Execution Result:" in captured.out
    assert "status" in captured.out
