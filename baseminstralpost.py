import os
import requests

API_KEY = "VJwU9oweEcylcc4WBVJzzfSgQZyuZXKE"  # store your key in env var
BASE_URL = "https://api.mistral.ai/v1"
ENDPOINT = f"{BASE_URL}/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}


data = {
    "model": "mistral-small-latest",  # or mistral-large-latest, etc.
    "messages": [
        {"role": "user", "content": "Hello from VS Code! What’s the weather like?"}
    ],
    "max_tokens": 100
}

def chat(prompt):
    data = {
    "model": "mistral-small-latest",  # or mistral-large-latest, etc.
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "max_tokens": 100}
    response = requests.post(ENDPOINT, json=data, headers=headers)
    return response.json()
   


response = requests.post(ENDPOINT, json=data, headers=headers)
print(response.json())