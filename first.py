import re
from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)


ingredients = input("Enter ingredients (comma-separated): ").strip()


if not ingredients:
    print("No ingredients provided. Please enter some ingredients.")
    exit()


prompt = f"Suggest a recipe using the following ingredients: {ingredients}. Use existing dishes only, do not create new ones."


completion = client.chat.completions.create(
  model="deepseek-ai/deepseek-r1",
  messages=[{"role":"user","content":prompt}],
  temperature=0.6,
  top_p=0.7,
  max_tokens=4096,
  stream=False  # Key change: Disable streaming
)

# Directly access the full response content
output = completion.choices[0].message.content


cleaned_output = re.sub(r'<think>.*?</think>', '', output, flags=re.DOTALL).strip()

print("\nGenerated Recipe:\n")
print(cleaned_output)
