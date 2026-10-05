"""E2E: the category/area filter bar narrows and resets visible results."""

import pytest

from tests.e2e.conftest import add_ingredients

pytestmark = pytest.mark.e2e


def test_filter_bar_narrows_results_by_category(app_page):
    page = app_page
    add_ingredients(page, "pork", "garlic")
    page.click("#search-btn")

    page.wait_for_selector("#results-section", state="visible")
    cards = page.locator("article.recipe-card")
    cards.first.wait_for(state="visible")
    assert cards.count() == 4

    filter_bar = page.locator("#filter-bar")
    filter_bar.wait_for(state="visible")
    veg_chip = page.locator('.filter-chip[data-value="Vegetarian"]')
    assert veg_chip.count() == 1

    veg_chip.click()
    page.wait_for_function(
        "() => document.querySelectorAll('article.recipe-card').length === 1"
    )
    assert cards.count() == 1
    assert cards.first.get_attribute("data-id") == "90003"

    all_chip = page.locator('.filter-chip[data-value=""]')
    all_chip.click()
    page.wait_for_function(
        "() => document.querySelectorAll('article.recipe-card').length === 4"
    )
    assert cards.count() == 4
