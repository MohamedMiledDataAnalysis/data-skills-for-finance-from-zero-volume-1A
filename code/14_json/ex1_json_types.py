# ex1_json_types.py - Exercise 1, JSON to Python and back
import json

text = ('{"customer_id": "C0042", "risk_rating": 4, '
        '"kyc_complete": true, "closed_on": null, '
        '"products": ["Mortgage", "Current"]}')
record = json.loads(text)
print(record["risk_rating"] + 1)
print(record["kyc_complete"], record["closed_on"])
print(len(record["products"]))
print(json.dumps(record, indent=4))
