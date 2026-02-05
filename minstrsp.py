import base64
import os 
import requests
import json

MINSTRAL_API_KEY = os.environ["MINSTRAL_API_KEY"]
BASE_URL = "https://api.mistral.ai/v1"
ENDPOINT = f"{BASE_URL}/chat/completions"

MINSTRAL_URL = "https://api.minstral.ai/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {MINSTRAL_API_KEY}",
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
   
js  = {"prompt":"What is the melting point of silver?"}
response = chat(js["prompt"])
print(response)
print("\n")
print(response['choices'][0]['message']['content'])
