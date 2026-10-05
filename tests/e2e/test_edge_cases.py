"""E2E: no-match empty state and backend validation error state."""

import pytest

from tests.e2e.conftest import add_ingredients

pytestmark = pytest.mark.e2e


def test_no_matching_recipes_shows_empty_state(app_page):
    page = app_page
    add_ingredients(page, "durian")

    page.click("#search-btn")

    page.wait_for_selector("#empty-state", state="visible")
    assert page.inner_text("#empty-state h3") == "No recipes found"
    assert "Try different ingredients" in page.inner_text("#empty-state p")
    assert page.locator("#results-section").is_hidden()


def test_invalid_ingredient_with_digits_shows_error_state(app_page):
    page = app_page
    add_ingredients(page, "pork2")

    page.click("#search-btn")

    page.wait_for_selector("#empty-state", state="visible")
    assert page.inner_text("#empty-state h3") == "Something went wrong"
    assert "numbers" in page.inner_text("#empty-state p")
    assert page.locator("#results-section").is_hidden()

    toast = page.locator("#toast")
    toast.wait_for(state="visible")
    assert "danger" in (toast.get_attribute("class") or "")
