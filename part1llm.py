import base64
import os 
import requests
import json
from flask import Flask, request

MINSTRAL_API_KEY = os.environ["MINSTRAL_API_KEY"]
BASE_URL = "https://api.mistral.ai/v1"
ENDPOINT = f"{BASE_URL}/chat/completions"

MINSTRAL_URL = "https://api.minstral.ai/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {MINSTRAL_API_KEY}",
}

app = Flask(__name__)



@app.route('/llm', methods=['POST'])
def response():
    js = request.get_json(silent=True) or {}
    prompt = js.get("prompt")
    response = chat(prompt)
    if not isinstance(prompt, str) or not prompt.strip():
        return {}, 400
    
    if response != None:
       print(response['choices'][0]['message']['content'])
       print(response)
       return {"output": response['choices'][0]['message']['content']}, 200
    elif response == None or response['choices'][0]['message']['content'] == "":
       return {}, 500


def chat(prompt):
    data = {
    "model": "mistral-small-latest",  # or mistral-large-latest, etc.
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "max_tokens": 500}
    response = requests.post(ENDPOINT, json=data, headers=headers)
    return response.json()
   



if __name__ == "__main__":
  app.run(host="localhost",port=3000)
