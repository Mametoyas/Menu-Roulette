"""Shared fixtures for the Playwright end-to-end suite.

These tests boot the real Flask app (src/web_app.py) on a local port and
drive it with a real browser via Playwright. TheMealDB is stubbed out —
src.api_client.BASE_URL is repointed at two fake routes registered on the
same Flask app, so no real network traffic to themealdb.com ever happens.
"""

import json
import socket
import threading
import time

import pytest
import requests
from flask import jsonify, request
from werkzeug.serving import make_server

from src import api_client, web_app

# ---------------------------------------------------------------------------
# Fake TheMealDB dataset
#
# Query "pork, garlic" is designed to match all four meals below (via the
# union of filter.php?i=pork and filter.php?i=garlic), with two meals
# scoring a full 1.0 (both ingredients present) and two scoring 0.5 (one
# ingredient present) — giving the roulette wheel >= 2 candidates and the
# modal test both "have" and "missing" ingredients to assert on.
# ---------------------------------------------------------------------------

FAKE_MEALS = {
    "90001": {
        "idMeal": "90001",
        "strMeal": "Pork Souvlaki",
        "strCategory": "Pork",
        "strArea": "Greek",
        "strMealThumb": "",
        "strInstructions": (
            "Marinate the pork in lemon and garlic.\n"
            "Grill until charred.\n"
            "Serve with lemon wedges."
        ),
        "strIngredient1": "Pork",
        "strIngredient2": "Garlic",
        "strIngredient3": "Lemon",
    },
    "90002": {
        "idMeal": "90002",
        "strMeal": "Garlic Butter Pork Chop",
        "strCategory": "Pork",
        "strArea": "American",
        "strMealThumb": "",
        "strInstructions": (
            "Season the pork chop.\n"
            "Sear in butter and garlic.\n"
            "Rest and serve."
        ),
        "strIngredient1": "Pork",
        "strIngredient2": "Garlic",
        "strIngredient3": "Butter",
    },
    "90003": {
        "idMeal": "90003",
        "strMeal": "Garlic Fried Rice",
        "strCategory": "Vegetarian",
        "strArea": "Thai",
        "strMealThumb": "",
        "strInstructions": (
            "Fry garlic until golden.\n"
            "Add rice and egg.\n"
            "Stir-fry and season."
        ),
        "strIngredient1": "Garlic",
        "strIngredient2": "Rice",
        "strIngredient3": "Egg",
    },
    "90004": {
        "idMeal": "90004",
        "strMeal": "Pork Belly Buns",
        "strCategory": "Pork",
        "strArea": "Chinese",
        "strMealThumb": "",
        "strInstructions": (
            "Braise the pork belly.\n"
            "Steam the buns.\n"
            "Assemble and serve."
        ),
        "strIngredient1": "Pork",
        "strIngredient2": "Sugar",
    },
}

FAKE_INDEX = {
    "pork": [
        {"idMeal": "90001", "strMeal": "Pork Souvlaki", "strMealThumb": ""},
        {"idMeal": "90002", "strMeal": "Garlic Butter Pork Chop", "strMealThumb": ""},
        {"idMeal": "90004", "strMeal": "Pork Belly Buns", "strMealThumb": ""},
    ],
    "garlic": [
        {"idMeal": "90001", "strMeal": "Pork Souvlaki", "strMealThumb": ""},
        {"idMeal": "90002", "strMeal": "Garlic Butter Pork Chop", "strMealThumb": ""},
        {"idMeal": "90003", "strMeal": "Garlic Fried Rice", "strMealThumb": ""},
    ],
}


def _free_port() -> int:
    """Returns an OS-assigned free TCP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def live_server():
    """Runs the real Flask app on a free local port with TheMealDB stubbed.

    Registers /__mealdb/filter.php and /__mealdb/lookup.php stub routes on
    the actual web_app.app instance, repoints api_client.BASE_URL at them,
    and serves everything through werkzeug's make_server (not app.run(),
    which would spawn a reloader that can't be shut down cleanly).
    """

    @web_app.app.route("/__mealdb/filter.php")
    def _fake_filter():
        ingredient = (request.args.get("i") or "").strip().lower()
        return jsonify({"meals": FAKE_INDEX.get(ingredient)})

    @web_app.app.route("/__mealdb/lookup.php")
    def _fake_lookup():
        meal_id = request.args.get("i")
        meal = FAKE_MEALS.get(meal_id)
        return jsonify({"meals": [meal] if meal else None})

    port = _free_port()
    api_client.BASE_URL = f"http://127.0.0.1:{port}/__mealdb"

    server = make_server("127.0.0.1", port, web_app.app, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    base_url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 10
    last_error = None
    while time.time() < deadline:
        try:
            requests.get(base_url, timeout=1)
            break
        except requests.exceptions.RequestException as e:
            last_error = e
            time.sleep(0.1)
    else:  # pragma: no cover - only hit if the server never comes up
        raise RuntimeError(f"live_server did not start in time: {last_error}")

    yield base_url

    server.shutdown()
    thread.join(timeout=5)


@pytest.fixture
def browser_context_args(browser_context_args):
    """Forces reduced-motion so the roulette wheel skips its 4.2s spin."""
    return {
        **browser_context_args,
        "reduced_motion": "reduce",
        "viewport": {"width": 1280, "height": 900},
    }


@pytest.fixture
def app_page(page, live_server):
    """A page loaded against the live stubbed server with clean localStorage."""
    page.goto(live_server)
    page.wait_for_selector("#search-btn", state="visible")
    page.evaluate("localStorage.clear()")
    page.reload()
    page.wait_for_selector("#search-btn", state="visible")
    return page


def add_ingredients(page, *names):
    """Types each ingredient into #ingredient-input and presses Enter."""
    input_box = page.locator("#ingredient-input")
    for name in names:
        input_box.fill(name)
        input_box.press("Enter")
    expected = len(set(names))
    page.wait_for_function(
        "(n) => document.querySelectorAll('#selected-ingredients .select-chip').length === n",
        arg=expected,
    )
    assert page.locator("#selected-ingredients .select-chip").count() == expected
