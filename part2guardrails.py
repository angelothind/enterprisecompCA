from ast import pattern
import base64
import os 
import requests
import json
from flask import Flask, request
import re

FIREBASE_URL = "https://guardrails-5c9b7-default-rtdb.europe-west1.firebasedatabase.app"

app = Flask(__name__)
"Creating guard rails"
@app.route('/guardrails/<id>', methods=['PUT'])
def create_guardrail(id):
    #Need to add code 200, 400 and 500 codes

    js = request.get_json(silent=True) or {}
    regx = js.get("regx")
    sub = js.get("sub")

    def is_valid_regex(pattern):
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False

    if not id or not regx or not sub:
        return {}, 400
    
    if is_valid_regex(regx) == False:
        return {}, 400
      # Bad Request

    guardrail = {
        "id": id,
        "regx": regx,
        "sub": sub
    }

    fb_url = f"{FIREBASE_URL}/guardrails/{id}.json"
    rsp = requests.put(fb_url, json=guardrail)
    print(rsp.status_code)

    if rsp.status_code != 200:
        return {}, 500  # Internal Server Error
    return {}, 201  # Created                
    

"Reading guard rails"
#Gets the json object with the same id as the id passed as parameter#
# GET /guardrails/id #
# returns the id regx and the sub#
@app.route('/guardrails/<id>', methods=['GET'])
def read_guardrail(id):
    fb_url = f"{FIREBASE_URL}/guardrails/{id}.json"
    rsp = requests.get(fb_url)
    print(rsp._content)

    if rsp.status_code != 200 or rsp.json() is None:
        print("This is being used")
        return {}, 404  # Not Found

    return rsp.json(), 200  # OK



"Delete  guard rails"
# DELETE /guardrails/id
# Delete guard rails by taking a json obeject with :
# in an "id" 
@app.route('/guardrails/<id>', methods=['DELETE'])
def delete_guardrail(id):
    fb_url = f"{FIREBASE_URL}/guardrails/{id}.json"
    rsp = requests.delete(fb_url)

    if rsp.status_code != 200:
        return {}, 500  # Internal Server Error
    
    return {}, 200  # OK

"Listing guard rails"
# GET /guardrails
# Returns a list of all guard rails#
@app.route('/guardrails', methods=['GET'])
def list_guardrails():
    fb_url = f"{FIREBASE_URL}/guardrails.json"
    rsp = requests.get(fb_url)

    if rsp.status_code != 200:
        return {}, 500  # Internal Server Error

    guardrails = rsp.json()
    if guardrails is None:
        guardrails = {}

    guardrail_list = list(guardrails.keys())
    return guardrail_list, 200  # OK

if __name__ == "__main__":
  app.run(host="localhost",port=3001)


