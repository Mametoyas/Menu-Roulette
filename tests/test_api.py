"""Unit tests for api_client.py using mocked HTTP responses."""

from unittest.mock import patch, MagicMock
import pytest
import requests
from src.api_client import (
    search_by_ingredient,
    get_meal_by_id,
    extract_ingredients,
    APIError,
)

MOCK_SEARCH_RESPONSE = {
    "meals": [
        {
            "idMeal": "52772",
            "strMeal": "Teriyaki Chicken Casserole",
            "strMealThumb": "",
        },
        {"idMeal": "52968", "strMeal": "Pork Souvlaki", "strMealThumb": ""},
    ]
}

MOCK_MEAL_DETAIL = {
    "meals": [
        {
            "idMeal": "52772",
            "strMeal": "Teriyaki Chicken Casserole",
            "strIngredient1": "chicken",
            "strIngredient2": "soy sauce",
            "strIngredient3": "garlic",
            "strIngredient4": "",
            # strIngredient5..20 จะเป็น "" หรือ None
        }
    ]
}


def make_mock_response(json_data: dict, status_code: int = 200) -> MagicMock:
    """Helper: สร้าง mock response object."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data
    return mock_resp


# --- search_by_ingredient ---

@patch("src.api_client.requests.get")
def test_search_by_ingredient_success(mock_get):
    """Returns list of meals when API responds with results."""
    mock_get.return_value = make_mock_response(MOCK_SEARCH_RESPONSE)
    result = search_by_ingredient("chicken")
    assert len(result) == 2
    assert result[0]["idMeal"] == "52772"


@patch("src.api_client.requests.get")
def test_search_by_ingredient_no_results(mock_get):
    """Returns empty list when API returns meals: null."""
    mock_get.return_value = make_mock_response({"meals": None})
    result = search_by_ingredient("avocado")
    assert result == []


@patch("src.api_client.requests.get")
def test_search_by_ingredient_api_error(mock_get):
    """Raises APIError on non-200 status code."""
    mock_get.return_value = make_mock_response({}, status_code=500)
    with pytest.raises(APIError):
        search_by_ingredient("chicken")


@patch("src.api_client.requests.get")
def test_search_by_ingredient_timeout(mock_get):
    """Raises APIError on request timeout."""
    mock_get.side_effect = requests.exceptions.Timeout
    with pytest.raises(APIError):
        search_by_ingredient("chicken")


# --- get_meal_by_id ---

@patch("src.api_client.requests.get")
def test_get_meal_by_id_success(mock_get):
    """Returns meal dict when ID is valid."""
    mock_get.return_value = make_mock_response(MOCK_MEAL_DETAIL)
    result = get_meal_by_id("52772")
    assert result["idMeal"] == "52772"
    assert result["strMeal"] == "Teriyaki Chicken Casserole"


@patch("src.api_client.requests.get")
def test_get_meal_by_id_not_found(mock_get):
    """Returns None when meal ID does not exist."""
    mock_get.return_value = make_mock_response({"meals": None})
    result = get_meal_by_id("99999")
    assert result is None


@patch("src.api_client.requests.get")
def test_get_meal_by_id_api_error(mock_get):
    """Raises APIError on non-200 status code."""
    mock_get.return_value = make_mock_response({}, status_code=500)
    with pytest.raises(APIError):
        get_meal_by_id("52772")


@patch("src.api_client.requests.get")
def test_get_meal_by_id_timeout(mock_get):
    """Raises APIError on request timeout."""
    mock_get.side_effect = requests.exceptions.Timeout
    with pytest.raises(APIError):
        get_meal_by_id("52772")


# --- extract_ingredients ---

def test_extract_ingredients_success():
    """Extracts non-empty ingredients from meal dict."""
    meal = MOCK_MEAL_DETAIL["meals"][0]
    result = extract_ingredients(meal)
    assert "chicken" in result
    assert "soy sauce" in result
    assert "garlic" in result


def test_extract_ingredients_skips_empty():
    """Does not include empty strIngredient fields."""
    meal = MOCK_MEAL_DETAIL["meals"][0]
    result = extract_ingredients(meal)
    assert "" not in result
