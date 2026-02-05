import requests
import unittest
#import database

LLM = "http://localhost:3000/llm"
GUARDRAILS = "http://localhost:3001/guardrails"
AUBERGE = "http://localhost:3002/auberge"

class Testing(unittest.TestCase):
  ############################################################
  ## test_001_llm				            ##
  ############################################################
  def test_001_llm(self):
    js  = {"prompt":"What is the melting point of silver?"}
    rsp = requests.post(LLM,json=js)

    self.assertEqual(rsp.status_code,200)
    self.assertTrue("961" in rsp.json()["output"])
