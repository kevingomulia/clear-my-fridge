import streamlit as st
import requests
import re
from src.util import is_match

API_KEY = st.secrets["auth"]["api_key"]
st.set_page_config(page_title="🥕 Fridge Cleaner", layout="wide")

st.title("🥕 Fridge Cleaner - Recipe Finder")

# --- Inputs ---
ingredients = st.text_input("Enter ingredients (comma-separated)", "chicken, garlic, onion")

style = st.selectbox(
    "Choose dish type / style",
    ["Any", "Soup", "Salad", "Main course", "Side dish", "Dessert", "Breakfast", "Snack", "Drink"]
)

if st.button("Find Recipes"):
    # --- Step 1: Search for recipes by style + ingredients ---
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "includeIngredients": ingredients,
        "number": 5,
        "apiKey": API_KEY,
    }
    if style != "Any":
        params["type"] = style.lower()

    res = requests.get(url, params=params)
    recipes = res.json().get("results", [])

    if not recipes:
        st.warning("No recipes found. Try different ingredients or style.")
    else:
        for r in recipes:
            # --- Step 2: Get detailed recipe info ---
            info_url = f"https://api.spoonacular.com/recipes/{r['id']}/information"
            info_params = {"includeNutrition": False, "apiKey": API_KEY}
            recipe = requests.get(info_url, params=info_params).json()

            col1, col2 = st.columns([1, 2])

            with col1:
                st.subheader(recipe["title"])
                st.image(recipe["image"], width='stretch')

            with col2:
                # --- Used vs Missing ingredients ---
                user_ingredients = [i.strip().lower() for i in ingredients.split(",")]
                used = [ing["name"] for ing in recipe.get("extendedIngredients", [])
                        if is_match(ing["name"], user_ingredients)]

                missing = [ing["name"] for ing in recipe.get("extendedIngredients", [])
                        if not is_match(ing["name"], user_ingredients)]

                st.markdown("**✅ Used ingredients:**")
                st.markdown(", ".join([f"`{u}`" for u in used]) if used else "None")

                st.markdown("**❌ Missing ingredients:**")
                st.markdown(", ".join([f"`{m}`" for m in missing]) if missing else "None")

                st.write(f"⏱️ Ready in {recipe.get('readyInMinutes', '?')} minutes")
                st.write(f"🍽️ Servings: {recipe.get('servings', '?')}")

            # --- Recipe summary (clean HTML tags) ---
            summary = re.sub("<[^<]+?>", "", recipe.get("summary", ""))

            with st.expander("📖 Quick Summary", expanded=True):
                st.write(summary)

            # --- Step-by-step instructions ---
            instructions = recipe.get("analyzedInstructions", [])
            if instructions:
                with st.expander("👩‍🍳 Cook It Yourself (Step-by-Step)", expanded=False):
                    for instr in instructions:
                        steps = instr.get("steps", [])
                        for step in steps:
                            st.markdown(f"**Step {step['number']}:** {step['step']}")
            else:
                st.info("No detailed instructions available.")

            # --- External link LAST ---
            st.markdown(f"[🔗 View Full Recipe Source]({recipe['sourceUrl']})")
            st.divider()