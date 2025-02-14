import streamlit as st
from transformers import pipeline

# Initialize the text generation pipeline
generator = pipeline('text-generation', model='gpt2')


def generate_recipe(ingredients, meal_type, cuisine):
    prompt = f"Generate a {cuisine} recipe for a {meal_type} using the following ingredients: {ingredients}.\n\nIngredients:\n\nInstructions:\n\nServing Size:\n\nNotes:"

    try:
        recipe = generator(
            prompt,
            max_length=750,  # Increased max_length
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7,
            num_beams=5,      # Added beam search
            no_repeat_ngram_size=2, # Prevent repetition
            early_stopping=True   # Stop when output plateaus
        )[0]['generated_text']

        recipe = recipe.replace(prompt, "").strip()
        return recipe
    except Exception as e:
        return f"Error generating recipe: {e}"


def main():
    st.title("Leftover Food Recipe Generator")
    st.write("Enter your ingredients, meal type, and cuisine preference.")

    ingredients = st.text_input("Ingredients (comma-separated):", "chicken, rice, vegetables")
    meal_type = st.selectbox("Meal Type:", ["Dinner", "Lunch", "Breakfast", "Snack"])
    cuisine = st.selectbox("Cuisine:", ["Italian", "Mexican", "Indian", "Chinese", "American"])

    if st.button("Generate Recipe"):
        if ingredients:
            with st.spinner("Generating recipe..."):
                recipe = generate_recipe(ingredients, meal_type, cuisine)
                st.subheader("Generated Recipe:")
                st.write(recipe)
        else:
            st.warning("Please enter ingredients.")


if __name__ == "__main__":
    main()