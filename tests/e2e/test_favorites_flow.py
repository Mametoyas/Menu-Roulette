"""E2E: add a favorite, view it on the Favorites tab, then remove it."""

import json

import pytest

from tests.e2e.conftest import add_ingredients

pytestmark = pytest.mark.e2e


def test_favorite_add_view_remove(app_page):
    page = app_page
    add_ingredients(page, "pork", "garlic")
    page.click("#search-btn")

    cards = page.locator("article.recipe-card")
    cards.first.wait_for(state="visible")

    first_fav_btn = page.locator("article.recipe-card .fav-btn").first
    first_fav_btn.click()

    page.wait_for_selector("article.recipe-card .fav-btn.active")
    assert first_fav_btn.evaluate("el => el.classList.contains('active')")

    stored = page.evaluate(
        "JSON.parse(localStorage.getItem('rr-favorites-v1') || '{}')"
    )
    assert len(stored.keys()) == 1

    assert page.inner_text("#fav-count") == "1"

    page.click("#nav-favorites")
    page.wait_for_selector("#results-section", state="visible")
    assert page.inner_text("#results-title") == "Favorite Recipes"
    assert page.locator("article.recipe-card").count() == 1

    page.click("article.recipe-card .fav-btn")

    page.wait_for_selector("#empty-state", state="visible")
    # The results grid is hidden (not removed) when empty, so assert on
    # visibility rather than DOM node count.
    assert page.locator("#results-section").is_hidden()
    assert page.locator("article.recipe-card:visible").count() == 0
    assert "No favorite recipes yet" in page.inner_text("#empty-state")

    fav_count = page.locator("#fav-count")
    assert "hidden" in (fav_count.get_attribute("class") or "")

    stored_after = page.evaluate(
        "JSON.parse(localStorage.getItem('rr-favorites-v1') || '{}')"
    )
    assert stored_after == {}
