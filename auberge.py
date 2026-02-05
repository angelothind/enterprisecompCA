import requests
import unittest
import database
import re
from flask import Flask, request

LLM = "http://localhost:3000/llm"
GUARDRAILS = "http://localhost:3001/guardrails"

app = Flask(__name__)


@app.route('/auberge', methods=['POST'])
def auberge():
    js = request.get_json(silent=True) or {}
    prompt = js.get("prompt")
    
    if not prompt:
        return {}, 400
    
    rsp = requests.get(f'{GUARDRAILS}')
    guardrail_ids = rsp.json()
    for id in guardrail_ids:
        rsp = requests.get(f'{GUARDRAILS}/{id}')
        guardrail = rsp.json()
        regx = guardrail["regx"]
        if re.search(regx, prompt):
            sub = guardrail["sub"]
            prompt = re.sub(regx, sub, prompt)

    rsp = requests.post(LLM, json={"prompt": prompt})
    output = rsp.json()["output"]
    print("LLM output before guardrails:", output)
    for id in guardrail_ids:
        rsp = requests.get(f'{GUARDRAILS}/{id}')
        guardrail = rsp.json()
        regx = guardrail["regx"]
        if re.search(regx, output):
            sub = guardrail["sub"]
            output = re.sub(regx, sub, output)

    print("LLM output after guardrails:", output)
    
    return {"output": output}, 200
  


if __name__ == "__main__":
    app.run(host="localhost",port=3002)
