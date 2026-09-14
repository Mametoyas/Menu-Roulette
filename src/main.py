"""Sprint 1 entry point verifying engine logic without GUI/CLI dependency."""

from src.utils import clean_ingredient_input, InvalidIngredientError
from src.recipe_engine import filter_recipes_by_ingredients, pick_random_recipe


def run_roulette_simulation(raw_input: str) -> dict:
    """Executes the pipeline: Clean -> Filter -> Random Pick."""
    try:
        cleaned_ingredients = clean_ingredient_input(raw_input)
        matches = filter_recipes_by_ingredients(cleaned_ingredients)
        selected = pick_random_recipe(matches)

        return {
            "status": "success",
            "query": cleaned_ingredients,
            "match_count": len(matches),
            "selected_recipe": selected,
        }
    except InvalidIngredientError as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # Test sample run
    sample_query = " Pork, Garlic "
    result = run_roulette_simulation(sample_query)
    print("Execution Result:", result)
