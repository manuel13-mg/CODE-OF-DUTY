import websocket
import json
import re
from openai import OpenAI


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

def generate_recipe(ingredients):
    prompt = prompt = f"Suggest a quick recipe with {ingredients}. Use only known dishes. Short output."

    completion = client.chat.completions.create(
    model="deepseek-ai/deepseek-r1",
    messages=[{"role":"user","content":prompt}],
    temperature=0.5,
    top_p=0.6,
    max_tokens=250, 
    stream=False
    )

    output = completion.choices[0].message.content
    cleaned_output = re.sub(r'<think>.*?</think>', '', output, flags=re.DOTALL).strip()
    return cleaned_output

def on_message(ws, message):
    request = json.loads(message)
    if 'ingredients' in request:
        recipe = generate_recipe(request['ingredients'])
        ws.send(json.dumps({"recipe": recipe}))

def on_open(ws):
    print("Connected to WebSocket server")

ws = websocket.WebSocketApp(
    "ws://localhost:8080",
    on_message=on_message,
    on_open=on_open
)

ws.run_forever()

