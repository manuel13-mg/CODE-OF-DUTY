import os
import re
import groq
import streamlit as st
import sqlite3
from datetime import datetime

# Set up Streamlit UI
st.title("🥗 Ingredient Expiry Tracker & Recipe Generator")
st.write("Enter ingredients with their expiry dates, and get recipe suggestions based on what's expiring soon!")

# Get the API key from Streamlit secrets
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY is not set. Please add it to `.streamlit/secrets.toml`.")
    st.stop()

# Initialize Groq client
client = groq.Client(api_key=api_key)

# Connect to SQLite database
conn = sqlite3.connect('ingredients.db', check_same_thread=False)
cursor = conn.cursor()

# Create a table to store ingredients and expiry dates
cursor.execute('''
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient TEXT NOT NULL,
    expiry_date TEXT NOT NULL
)
''')
conn.commit()

# Function to add ingredient to the database
def add_ingredient(ingredient, expiry_date):
    try:
        cursor.execute('INSERT INTO ingredients (ingredient, expiry_date) VALUES (?, ?)', (ingredient, expiry_date))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"❌ Database Error: {e}")
        return False

# Function to get the top few ingredients closest to expiry
def get_top_expiry_ingredients(limit=4):
    try:
        cursor.execute('SELECT ingredient, expiry_date FROM ingredients ORDER BY expiry_date ASC LIMIT ?', (limit,))
        return cursor.fetchall()
    except Exception as e:
        st.error(f"❌ Database Error: {e}")
        return []

# Function to generate a recipe using Groq API
def generate_recipe(ingredients):
    ingredient_list = ', '.join([ingredient for ingredient, _ in ingredients])
    prompt = f"Suggest a recipe using the following ingredients: {ingredient_list}. Use existing dishes only, do not create new ones. Prioritize recipes with the closest expiry date first."

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.6,
            top_p=0.7
        )

        # ✅ Access response correctly
        output = response.choices[0].message.content

        # ✅ Remove unnecessary tags (if any)
        cleaned_output = re.sub(r'</think>.*?</think>', '', output, flags=re.DOTALL).strip()
        return cleaned_output

    except Exception as e:
        st.error(f"❌ Recipe Generation Error: {e}")
        return None

# Streamlit UI for adding ingredients
st.subheader("🛒 Add Ingredients")
ingredient_input = st.text_input("Enter Ingredient Name")
expiry_date_input = st.date_input("Select Expiry Date")

if st.button("➕ Add Ingredient"):
    if ingredient_input and expiry_date_input:
        formatted_date = expiry_date_input.strftime("%Y-%m-%d")
        if add_ingredient(ingredient_input, formatted_date):
            st.success(f"✅ Added: {ingredient_input} (Expiry: {formatted_date})")
    else:
        st.warning("⚠️ Please enter both an ingredient and an expiry date.")

# Generate recipe using the top few ingredients closest to expiry
if st.button("🍽️ Generate Recipe"):
    top_ingredients = get_top_expiry_ingredients()
    if top_ingredients:
        st.write("📌 Using ingredients with closest expiry dates:")
        for ingredient, expiry_date in top_ingredients:
            st.write(f"🔹 {ingredient} (Expiry Date: {expiry_date})")

        recipe = generate_recipe(top_ingredients)
        if recipe:
            st.subheader("✨ Suggested Recipe")
            st.write(recipe)
    else:
        st.warning("⚠️ No ingredients found in the database.")

# Close the database connection
conn.close()
