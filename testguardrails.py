GUARDRAILS = "http://localhost:3001/guardrails"
import requests
import unittest
import database
import re

class Testing(unittest.TestCase):
    def test_002_guardrails(self):
        database.db.clear()

        id   = "931"
        regx = r"Prince Andrew"
        sub  = "Andrew Mountbatten-Windsor"
        js   = {"id":id,"regx":regx,"sub":sub}

        rsp = requests.put(f'{GUARDRAILS}/{id}',json=js)
        self.assertEqual(rsp.status_code,201)

        rsp = requests.get(f'{GUARDRAILS}/{id}')
        self.assertEqual(rsp.status_code,200)
        self.assertEqual(id,rsp.json()["id"])
        self.assertEqual(regx,rsp.json()["regx"])
        self.assertEqual(sub,rsp.json()["sub"])


    def test_003_guardrails(self):
        database.db.clear()
        
        id   = "email-001"
        regx = r"[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+" 
        sub  = "<Email address>"
        js   = {"id":id,"regx":regx,"sub":sub}

        rsp = requests.put(f'{GUARDRAILS}/{id}',json=js)
        self.assertEqual(rsp.status_code,201)

        rsp = requests.get(f'{GUARDRAILS}/{id}')
        self.assertEqual(rsp.status_code,200)
        self.assertEqual(id,rsp.json()["id"])
        self.assertEqual(regx,rsp.json()["regx"])
        self.assertEqual(sub,rsp.json()["sub"])

    ############################################################
  ## test_004_guardrails				    ##
  ############################################################
    def test_004_guardrails(self):
        database.db.clear()

        id   = "Broken"
        regx = r"*a-z]" 
        sub  = "anything"
        js   = {"id":id,"regx":regx,"sub":sub}

        rsp = requests.put(f'{GUARDRAILS}/{id}',json=js)
        self.assertEqual(rsp.status_code,400) # Bad input
    
    def test_005_guardrails(self):
        database.db.clear()
        rsp = requests.get(f'{GUARDRAILS}')
        self.assertEqual(rsp.status_code,200)
        ids_list = rsp.json()
        current_count = len(ids_list)
        requests.put(f'{GUARDRAILS}/test-001',json={"id":"addition","regx":r"test","sub":"<test1>"})
        rsp = requests.get(f'{GUARDRAILS}')
        self.assertEqual(rsp.status_code,200)
        ids_list = rsp.json()
        self.assertEqual(len(ids_list), current_count + 1)

    def test_006_guardrails(self):
        database.db.clear()     
        rsp = requests.get(f'{GUARDRAILS}')
        self.assertEqual(rsp.status_code,200)
        ids_list = rsp.json()
        current_count = len(ids_list)
        for id in ids_list:
            requests.delete(f'{GUARDRAILS}/{id}')
            rsp = requests.get(f'{GUARDRAILS}')
            size = len(rsp.json())
            self.assertEqual(size, current_count - 1)
            current_count = size

    def test_007_guardrails(self):
        database.db.clear()
        id1   = "guardrail-001"
        regx1 = r"\bgrail\b"
        sub1  = "<grail>"
        object1   = {"id":id1,"regx":regx1,"sub":sub1}
    
        id2 = "grail2"
        regx2 = r"\bgrail2\b"
        sub2  = "<grail2>"
        object2   = {"id":id2,"regx":regx2,"sub":sub2}

        rsp = requests.put(f'{GUARDRAILS}/{id1}',json=object1)
        self.assertEqual(rsp.status_code,201)
        rsp = requests.put(f'{GUARDRAILS}/{id2}',json=object2)
        self.assertEqual(rsp.status_code,201)
        rsp = requests.get(f'{GUARDRAILS}')
        self.assertEqual(rsp.status_code,200)
        ids_list = rsp.json()
        self.assertEqual(len(ids_list), 2)
        self.assertIn(id1, ids_list)
        self.assertIn(id2, ids_list)

    def test_008_guardrails(self):
        database.db.clear()     
        rsp = requests.get(f'{GUARDRAILS}')
        self.assertEqual(rsp.status_code,200)
        ids_list = rsp.json()
        current_count = len(ids_list)
        for id in ids_list:
            requests.delete(f'{GUARDRAILS}/{id}')
            rsp = requests.get(f'{GUARDRAILS}')
            size = len(rsp.json())
            self.assertEqual(size, current_count - 1)
            current_count = size