import sqlite3
import re
import groq
from datetime import datetime

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('ingredients.db')
cursor = conn.cursor()

# Create a table to store ingredients and their expiry dates
cursor.execute('''
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient TEXT NOT NULL,
    expiry_date TEXT NOT NULL
)
''')
conn.commit()

# Function to add ingredient and expiry date to the database
def add_ingredient(ingredient, expiry_date):
    cursor.execute('''
    INSERT INTO ingredients (ingredient, expiry_date)
    VALUES (?, ?)
    ''', (ingredient, expiry_date))
    conn.commit()

# Function to get the top few ingredients closest to expiry
def get_top_expiry_ingredients(limit=4):
    cursor.execute('''
    SELECT ingredient, expiry_date FROM ingredients
    ORDER BY expiry_date ASC LIMIT ?
    ''', (limit,))
    return cursor.fetchall()

# Initialize Groq client
client = groq.Client(api_key="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")  # Replace with your API key

# Function to generate recipe using Groq
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

        # ✅ Fix: Access response correctly
        output = response.choices[0].message.content

        # Apply regex to clean the output by removing text between </think> tags
        cleaned_output = re.sub(r'</think>.*?</think>', '', output, flags=re.DOTALL).strip()
        return cleaned_output

    except Exception as e:
        return f"An error occurred: {e}"

# User inputs ingredients and expiry date until "exit" is entered or at least 12 values are entered
entry_count = 0
while entry_count < 12:
    ingredient_input = input("Enter ingredient (or type 'exit' to finish): ").strip()
    if ingredient_input.lower() == 'exit':
        break
    expiry_date_input = input("Enter expiry date (YYYY-MM-DD): ").strip()
    
    # Validate date format
    try:
        datetime.strptime(expiry_date_input, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        continue

    if ingredient_input and expiry_date_input:
        add_ingredient(ingredient_input, expiry_date_input)
        entry_count += 1
        print(f"Added {ingredient_input} with expiry date {expiry_date_input} to the database.")
    else:
        print("Please enter both ingredient and expiry date.")

# Close the database connection after data entry
conn.close()

# Reconnect to the database to read data for recipe generation
conn = sqlite3.connect('ingredients.db')
cursor = conn.cursor()

# Generate recipe using the top few ingredients closest to expiry
top_ingredients = get_top_expiry_ingredients()
if top_ingredients:
    print("\nUsing ingredients with closest expiry dates:")
    for ingredient, expiry_date in top_ingredients:
        print(f"{ingredient} (Expiry Date: {expiry_date})")

    recipe = generate_recipe(top_ingredients)
    print("\nGenerated Recipe:\n")
    print(recipe)
else:
    print("No ingredients found in the database.")

# Close the database connection
conn.close()
