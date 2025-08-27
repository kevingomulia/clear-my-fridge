from rapidfuzz import fuzz

def is_match(recipe_ing: str, user_ings: list[str], threshold: int = 80) -> bool:
    """Check if recipe ingredient matches any user ingredient (fuzzy)."""
    recipe_ing = recipe_ing.lower()
    return any(fuzz.partial_ratio(user_ing, recipe_ing) >= threshold for user_ing in user_ings)