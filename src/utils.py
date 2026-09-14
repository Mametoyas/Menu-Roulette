"""Utility functions for string manipulation and input validation."""

import re


class InvalidIngredientError(ValueError):
    """Raised when the input contains invalid characters or numbers."""

    pass


def clean_ingredient_input(raw_input: str) -> list[str]:
    """Cleans and parses raw ingredient inputs from user.

    Args:
        raw_input (str): Raw comma-separated string (e.g., " Pork , Egg! ")

    Returns:
        list[str]: Cleaned list of unique ingredient names in lowercase.

    Raises:
        InvalidIngredientError: If input is empty or contains numbers.
    """
    if not raw_input or not raw_input.strip():
        raise InvalidIngredientError("Input cannot be empty.")

    # Reject numbers in ingredient strings
    if re.search(r"\d", raw_input):
        raise InvalidIngredientError("Ingredients must not contain numbers.")

    # Split by comma, strip whitespace, remove empty elements,
    # and convert to lowercase
    raw_list = raw_input.split(",")
    cleaned = []

    for item in raw_list:
        # Remove non-alphanumeric trailing/leading characters except spaces
        item_clean = re.sub(r"[^\w\s]", "", item).strip().lower()
        if item_clean and item_clean not in cleaned:
            cleaned.append(item_clean)

    if not cleaned:
        err_msg = "No valid ingredients found after sanitization."
        raise InvalidIngredientError(err_msg)

    return cleaned
