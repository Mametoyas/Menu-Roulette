"""Unit tests for the Flask web application (src/web_app.py)."""

from unittest.mock import patch

import pytest

from src import web_app
from src.web_app import app

RAW_MEAL = {
    "idMeal": "52968",
    "strMeal": "Pork Souvlaki",
    "strCategory": "Pork",
    "strArea": "Greek",
    "strMealThumb": "http://img/pork-souvlaki.jpg",
    "strInstructions": "Mix pork with lemon and garlic.\nGrill and serve.",
    "strIngredient1": "pork",
    "strIngredient2": "garlic",
    "strIngredient3": "lemon",
}

FORMATTED = web_app.format_recipe(RAW_MEAL)


@pytest.fixture
def client():
    """Flask test client for the web application."""
    with app.test_client() as test_client:
        yield test_client


def test_index_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "fridge" in resp.get_data(as_text=True).lower()


@patch("src.web_app.run_roulette_simulation")
def test_api_search_success(mock_run, client):
    mock_run.return_value = {
        "status": "success",
        "query": ["pork", "garlic"],
        "match_count": 1,
        "selected_recipe": FORMATTED,
        "top_recipes": [FORMATTED],
    }
    resp = client.post("/api/search", json={"ingredients": "pork, garlic"})

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "success"
    assert data["match_count"] == 1
    assert data["top_recipes"][0]["name"] == "Pork Souvlaki"
    assert data["selected_recipe"]["ingredients"] == [
        "pork",
        "garlic",
        "lemon",
    ]
    mock_run.assert_called_once_with("pork, garlic")


@patch("src.web_app.run_roulette_simulation")
def test_api_search_invalid_input(mock_run, client):
    mock_run.return_value = {
        "status": "error",
        "message": "Ingredients must not contain numbers.",
    }
    resp = client.post("/api/search", json={"ingredients": "pork 123"})

    assert resp.status_code == 200
    assert resp.get_json()["status"] == "error"


@patch("src.web_app.run_roulette_simulation")
def test_api_search_api_error(mock_run, client):
    mock_run.return_value = {"status": "error", "message": "API failed"}
    resp = client.post("/api/search", json={"ingredients": "chicken"})

    assert resp.status_code == 200
    assert resp.get_json()["message"] == "API failed"


@patch("src.web_app.get_meal_by_id")
def test_recipe_detail(mock_get, client):
    mock_get.return_value = RAW_MEAL
    resp = client.get("/recipe/52968")

    assert resp.status_code == 200
    body = resp.get_json()
    assert body["name"] == "Pork Souvlaki"
    assert body["area"] == "Greek"
    assert body["ingredients"] == ["pork", "garlic", "lemon"]
    assert body["instructions"] == (
        "Mix pork with lemon and garlic.\nGrill and serve."
    )


@patch("src.web_app.get_meal_by_id")
def test_recipe_detail_not_found(mock_get, client):
    mock_get.return_value = None
    resp = client.get("/recipe/99999")
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "Recipe not found"
