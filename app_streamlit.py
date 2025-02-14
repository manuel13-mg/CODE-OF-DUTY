import re
import streamlit as st
from openai import OpenAI

# --- Initialize OpenAI Client ---
try:
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key="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"  # **SECURE API KEY!** Use environment variables.
    )
    model_available = True #Boolean value to access code only if model is running
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}")
    model_available = False

# --- App Title and Description ---
st.title("Recipe Generator")
st.markdown("Enter ingredients (comma-separated) to get a recipe suggestion.")

# --- Input Area ---
ingredients = st.text_input("Ingredients (comma-separated):")

# --- Generate Recipe Button ---
if st.button("Generate Recipe") and model_available:
    if not ingredients:
        st.warning("Please enter some ingredients.")
    else:
        # --- Create the prompt for the recipe generator ---
        prompt = f"Suggest a recipe using the following ingredients: {ingredients}. Use existing dishes only, do not create new ones."

        # --- API call (stream=False) ---
        try:
            completion = client.chat.completions.create(
                model="deepseek-ai/deepseek-r1",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                top_p=0.7,
                max_tokens=4096,
                stream=False
            )

            # --- Access and Clean Response ---
            output = completion.choices[0].message.content
            cleaned_output = re.sub(r'<think>.*?</think>', '', output, flags=re.DOTALL).strip()

            # --- Display Recipe ---
            st.subheader("Generated Recipe:")
            st.write(cleaned_output) #Displays message

        except Exception as e:
            st.error(f"Error generating recipe: {e}")

# --- Run the app ---
# To run, save as a .py file (e.g., recipe_app.py) and then:
# 1. Open your terminal or command prompt.
# 2. Navigate to the directory where you saved the file.
# 3. Run the command: streamlit run recipe_app.py