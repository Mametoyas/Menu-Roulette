"""E2E: the roulette wheel picks a winner and opens its recipe modal."""

import pytest

from tests.e2e.conftest import add_ingredients

pytestmark = pytest.mark.e2e


def test_roulette_spins_and_picks_winner(app_page):
    page = app_page
    add_ingredients(page, "pork", "garlic")

    page.click("#roulette-btn")

    page.wait_for_selector("#wheel-canvas", state="visible")
    winner = page.locator("li.wheel-legend-item.wheel-winner")
    winner.first.wait_for(state="attached", timeout=8000)
    assert winner.count() == 1

    winner_id = winner.first.get_attribute("data-id")
    assert winner_id
    winner_name = winner.first.inner_text().strip()

    view_btn = page.locator("#wheel-view")
    view_btn.wait_for(state="visible", timeout=8000)
    view_btn.click(force=True)

    modal = page.locator("#recipe-modal")
    modal.wait_for(state="visible")
    assert page.locator("#wheel-canvas").count() == 0
    assert winner_name in modal.inner_text()
