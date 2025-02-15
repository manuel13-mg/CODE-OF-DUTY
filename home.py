import re
import streamlit as st
import groq

# --- Configuration ---
st.set_page_config(
    page_title="Recipe Generator",
    page_icon=":fork_and_knife:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- CSS Styling ---
st.markdown(
    """
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f0f2f6;
        color: #262730;
    }

    .stApp {
        max-width: 800px;
        margin: 0 auto;
        padding: 30px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    h1 {
        color: #000000 !important; /* Black for the header and !important */
        text-align: center;
    }

    .stTextInput>label {
        color: #000000;
    }

    .stButton>button {
        background-color: #e44d26;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #d23211;
    }

    .stAlert {
        background-color: #fce8e6;
        color: #e44d26;
        border: 1px solid #e44d26;
        border-radius: 5px;
        padding: 10px;
        margin-top: 10px;
    }
    .page-label>label {
        color: #000000 !important; /* Black for the page labels */
    }

    .recipe-output {
        margin-top: 20px;
        padding: 15px;
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 5px;
        white-space: pre-wrap;
        color: #000000;
        font-size: 1.1em;
    }
    p {
        color: #000000; /* Black for paragraph text */
    }
    #generated-recipe {
        color: #000000; /* Black for the element with id="generated-recipe" */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Initialize Groq Client ---
try:
    groq_api_key = "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"  # Use the provided API key
    client = groq.Client(api_key=groq_api_key)
    model_available = True
except Exception as e:
    st.error(f"Error initializing Groq client: {e}")
    model_available = False

def get_recipe(ingredients, cuisine, meal_type):
    """
    Generate a recipe using the given ingredients, cuisine, and meal type.

    Args:
        ingredients (str): Comma-separated list of ingredients.
        cuisine (str): The desired cuisine ("Any" for no preference).
        meal_type (str): The desired meal type ("Any" for no preference).

    Returns:
        str: The generated recipe.
    """

    # Create the prompt for the recipe generator
    prompt = f"Suggest a recipe using the following ingredients: {ingredients}. "
    if cuisine != "Any":
        prompt += f"It should be a {cuisine} recipe. "
    if meal_type != "Any":
        prompt += f"It should be a {meal_type} meal. "
    prompt += "Use existing dishes only, do not create new ones."

    try:
        # Generate the recipe using Groq
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Groq supports Mixtral for better text generation
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.6,
            top_p=0.7
        )

        # Extract response text
        output = response.choices[0].message.content

        # Apply regex to clean the output by removing text between <think> tags
        cleaned_output = re.sub(r'<think>.*?</think>', '', output, flags=re.DOTALL).strip()

        return cleaned_output

    except Exception as e:
        st.error(f"Error generating recipe: {e}")
        return None

# --- Streamlit App ---
st.title("Recipe Generator")
st.markdown("Enter ingredients to get a recipe suggestion.")

# --- Ingredients Input ---
ingredients = st.text_input("Ingredients (comma-separated):",
                             placeholder="e.g., chicken, rice, vegetables",
                             help="Separate ingredients with commas.")

# --- Select boxes for Cuisine and Meal type
cuisine = st.selectbox(
    "Cuisine:",
    options=["Any", "Italian", "Indian", "Mexican", "Chinese", "American", "French"],
    index=0,
    help="Select the desired cuisine."
)

meal_type = st.selectbox(
    "Meal Type:",
    options=["Any", "Dinner", "Lunch", "Breakfast", "Snack", "Dessert"],
    index=0,
    help="Select the desired meal type."
)

# --- Generate Recipe Button ---
if st.button("Generate Recipe") and model_available:
    if not ingredients:
        st.warning("Please enter some ingredients.")
    else:
        recipe = get_recipe(ingredients, cuisine, meal_type)

        if recipe:
            st.subheader("Generated Recipe:")
            st.markdown(f'<div class="recipe-output">{recipe}</div>', unsafe_allow_html=True)
        else:
            st.error("Failed to generate recipe.")
