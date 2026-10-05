"""E2E: copying a recipe's missing-ingredient shopping list to the clipboard."""

import pytest

from tests.e2e.conftest import add_ingredients

pytestmark = pytest.mark.e2e


def test_copy_shopping_list_to_clipboard(app_page):
    page = app_page
    page.context.grant_permissions(["clipboard-read", "clipboard-write"])

    add_ingredients(page, "garlic")
    page.click("#search-btn")

    page.wait_for_selector("#results-section", state="visible")
    cards = page.locator("article.recipe-card")
    cards.first.wait_for(state="visible")

    # "Pork Souvlaki" (90001) needs Pork/Garlic/Lemon; the user only has
    # garlic, so Pork and Lemon are missing -- giving a non-empty shopping
    # list and a #copy-shopping button in the modal.
    souvlaki_card = page.locator('article.recipe-card[data-id="90001"]')
    souvlaki_card.wait_for(state="visible")
    souvlaki_card.click()

    modal = page.locator("#recipe-modal")
    modal.wait_for(state="visible")

    copy_btn = page.locator("#copy-shopping")
    copy_btn.wait_for(state="visible")
    copy_btn.click()

    # The toast element always exists in the DOM with opacity-0 (so Playwright
    # considers it "visible" from page load), and copyShopping() only fills in
    # its text/"visible" class asynchronously once the clipboard promise
    # resolves. Wait for that class (not just DOM visibility) before reading.
    toast = page.locator("#toast")
    page.wait_for_function(
        "() => document.getElementById('toast').classList.contains('visible')"
    )
    assert "copied" in toast.inner_text().lower()

    clipboard_text = page.evaluate("() => navigator.clipboard.readText()")
    lower = clipboard_text.lower()
    assert "pork souvlaki" in lower
    assert "pork" in lower
    assert "lemon" in lower
    assert "garlic" not in lower
