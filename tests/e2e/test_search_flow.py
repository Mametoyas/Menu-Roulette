"""E2E: ingredient search renders result cards, counts, and recipe modal."""

import re

import pytest

from tests.e2e.conftest import add_ingredients

pytestmark = pytest.mark.e2e


def test_search_renders_cards_and_count(app_page):
    page = app_page
    add_ingredients(page, "pork", "garlic")

    page.click("#search-btn")

    page.wait_for_selector("#results-section", state="visible")
    cards = page.locator("article.recipe-card")
    cards.first.wait_for(state="visible")

    # All four fake meals match the union of "pork" and "garlic" filters.
    assert cards.count() == 4
    assert page.inner_text("#results-title") == "Matched Recipes"

    count_text = page.inner_text("#results-count")
    assert re.search(r"4 of 4 matching recipes? for: pork, garlic", count_text)


def test_card_opens_modal_with_grouped_ingredients(app_page):
    page = app_page
    add_ingredients(page, "pork", "garlic")
    page.click("#search-btn")

    cards = page.locator("article.recipe-card")
    cards.first.wait_for(state="visible")
    cards.first.click()

    modal = page.locator("#recipe-modal")
    modal.wait_for(state="visible")
    # headings are rendered uppercase via CSS text-transform, so compare
    # case-insensitively against the raw rendered text.
    modal_text = modal.inner_text().lower()
    assert "in your kitchen" in modal_text
    assert "need to buy" in modal_text

    have_items = modal.locator("li.ingredient-item:not(.missing)")
    missing_items = modal.locator("li.ingredient-item.missing")
    assert have_items.count() >= 2
    assert missing_items.count() >= 1

    page.click(".modal-close")
    page.wait_for_selector("#recipe-modal", state="hidden")


def test_quick_chip_adds_ingredient(app_page):
    page = app_page
    page.click('.quick-chip[data-ingredient="pork"]')

    chips = page.locator("#selected-ingredients .select-chip")
    chips.first.wait_for(state="visible")
    assert chips.count() == 1
    assert chips.first.inner_text().strip() == "pork"
