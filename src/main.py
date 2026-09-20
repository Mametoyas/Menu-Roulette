"""Console entry point — Sprint 2 live TheMealDB API flow."""

# Import supports both execution modes:
#   python src/main.py      -> utils / recipe_engine / api_client (src/ on sys.path)
#   pytest (pythonpath = .) -> src.utils / src.recipe_engine / src.api_client
try:  # pragma: no cover - exercised when running `python src/main.py`
    from utils import clean_ingredient_input, InvalidIngredientError
    from recipe_engine import filter_and_rank, pick_random_recipe
    from api_client import APIError
except ImportError:
    from src.utils import clean_ingredient_input, InvalidIngredientError
    from src.recipe_engine import filter_and_rank, pick_random_recipe
    from src.api_client import APIError


def run_roulette_simulation(raw_input: str) -> dict:
    """Executes the pipeline: Clean -> Live API Search/Score/Rank -> Random Pick."""
    try:
        cleaned_ingredients = clean_ingredient_input(raw_input)
        ranked = filter_and_rank(cleaned_ingredients)
        selected = pick_random_recipe(ranked)

        return {
            "status": "success",
            "query": cleaned_ingredients,
            "match_count": len(ranked),
            "selected_recipe": selected,
        }
    except InvalidIngredientError as e:
        return {"status": "error", "message": str(e)}
    except APIError as e:
        return {"status": "error", "message": str(e)}


def run_console() -> None:
    """Runs the interactive input()/print() roulette session."""
    sample_query = input("Enter the ingredients (example: 'Pork, Garlic'):")
    result = run_roulette_simulation(sample_query)
    print("Execution Result:", result)


if __name__ == "__main__":  # pragma: no cover
    run_console()
