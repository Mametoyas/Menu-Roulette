"""E2E: clearing results and the "no ingredients selected" guard toasts."""

import pytest

from tests.e2e.conftest import add_ingredients

pytestmark = pytest.mark.e2e


def test_clear_results_resets_everything(app_page):
    page = app_page
    add_ingredients(page, "pork", "garlic")
    page.click("#search-btn")

    page.wait_for_selector("#results-section", state="visible")
    page.locator("article.recipe-card").first.wait_for(state="visible")
    page.wait_for_selector("#filter-bar", state="visible")

    page.click("#clear-results")

    assert page.locator("#results-section").is_hidden()
    assert page.locator("#results-grid article.recipe-card").count() == 0
    assert page.locator("#selected-ingredients .select-chip").count() == 0
    assert page.locator("#filter-bar").count() == 0


def test_search_without_ingredients_shows_warning_toast(app_page):
    page = app_page
    assert page.locator("#selected-ingredients .select-chip").count() == 0

    page.click("#search-btn")

    toast = page.locator("#toast")
    toast.wait_for(state="visible")
    assert "Add at least one ingredient" in toast.inner_text()
    assert "danger" in (toast.get_attribute("class") or "")


def test_roulette_without_ingredients_shows_warning_toast(app_page):
    page = app_page
    assert page.locator("#selected-ingredients .select-chip").count() == 0

    page.click("#roulette-btn")

    toast = page.locator("#toast")
    toast.wait_for(state="visible")
    assert "Add at least one ingredient" in toast.inner_text()
    assert "danger" in (toast.get_attribute("class") or "")
