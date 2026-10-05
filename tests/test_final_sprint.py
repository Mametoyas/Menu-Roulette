"""Final sprint part 1 tests - roulette wheel data contract."""

# Tests the server payload the canvas wheel consumes:
# top_recipes (id + name candidates) and selected_recipe (the winner).
# All backend calls are mocked - no network access.

from unittest.mock import patch

import pytest

from src.web_app import app


def make_recipe(meal_id, name, score=1.0):
    """Builds a formatted recipe dict as produced by format_recipe()."""
    return {
        "id": meal_id,
        "name": name,
        "category": "Pork",
        "area": "Greek",
        "image_url": "http://img/x.jpg",
        "ingredients": ["pork", "garlic"],
        "instructions": "Grill and serve.",
        "youtube_url": "",
        "score": score,
    }


@pytest.fixture
def client():
    """Flask test client for the web application."""
    with app.test_client() as test_client:
        yield test_client


@patch("src.web_app.run_roulette_simulation")
def test_wheel_payload_has_candidates_and_winner(mock_run, client):
    """Wheel needs >=2 named candidates and a winner among them."""
    top = [
        make_recipe("1", "Pork Souvlaki"),
        make_recipe("2", "Garlic Pork"),
        make_recipe("3", "Lemon Pork"),
    ]
    mock_run.return_value = {
        "status": "success",
        "query": ["pork"],
        "match_count": 3,
        "selected_recipe": top[1],
        "top_recipes": top,
    }

    data = client.post("/api/search", json={"ingredients": "pork"}).get_json()

    assert data["status"] == "success"
    assert len(data["top_recipes"]) >= 2
    assert all(r["id"] and r["name"] for r in data["top_recipes"])
    top_ids = {str(r["id"]) for r in data["top_recipes"]}
    assert str(data["selected_recipe"]["id"]) in top_ids


@patch("src.web_app.run_roulette_simulation")
def test_wheel_single_candidate_falls_back_to_modal(mock_run, client):
    """One candidate carries enough data for the direct modal path."""
    only = make_recipe("9", "Lonely Pork")
    mock_run.return_value = {
        "status": "success",
        "query": ["pork"],
        "match_count": 1,
        "selected_recipe": only,
        "top_recipes": [only],
    }

    data = client.post("/api/search", json={"ingredients": "pork"}).get_json()

    assert len(data["top_recipes"]) == 1
    assert data["selected_recipe"]["name"] == "Lonely Pork"


@patch("src.web_app.run_roulette_simulation")
def test_wheel_empty_result_has_no_winner(mock_run, client):
    """Empty results must not produce a winner payload."""
    mock_run.return_value = {
        "status": "success",
        "query": ["avocado"],
        "match_count": 0,
        "selected_recipe": None,
        "top_recipes": [],
    }

    data = client.post("/api/search", json={"ingredients": "avocado"}).get_json()

    assert data["top_recipes"] == []
    assert data["selected_recipe"] is None


@patch("src.web_app.run_roulette_simulation")
def test_wheel_winner_comes_from_top_scores(mock_run, client):
    """Winner id matches one of the top-scored candidates."""
    top = [
        make_recipe("1", "Low Pork", score=0.5),
        make_recipe("2", "Top Pork A", score=1.0),
        make_recipe("3", "Top Pork B", score=1.0),
    ]
    mock_run.return_value = {
        "status": "success",
        "query": ["pork"],
        "match_count": 3,
        "selected_recipe": top[2],
        "top_recipes": top,
    }

    data = client.post("/api/search", json={"ingredients": "pork"}).get_json()

    best = max(r["score"] for r in data["top_recipes"])
    assert data["selected_recipe"]["score"] == best
