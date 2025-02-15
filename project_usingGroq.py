import re
import groq

def get_recipe(ingredients):
    """
    Generate a recipe using the given ingredients.

    Args:
        ingredients (str): Comma-separated list of ingredients.

    Returns:
        str: The generated recipe.
    """
    # Initialize the Groq client
    client = groq.Client(api_key="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")

    # Create the prompt for the recipe generator
    prompt = f"Suggest a recipe using the following ingredients: {ingredients}. Use existing dishes only, do not create new ones."

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
        print(f"An error occurred: {e}")
        return None

def main():
    # User inputs ingredients
    ingredients = input("Enter ingredients (comma-separated): ").strip()

    # Check if ingredients were provided
    if not ingredients:
        print("No ingredients provided. Please enter some ingredients.")
        return

    recipe = get_recipe(ingredients)

    if recipe:
        # Print the generated recipe
        print("\nGenerated Recipe:\n")
        print(recipe)

if __name__ == "__main__":
    main()
