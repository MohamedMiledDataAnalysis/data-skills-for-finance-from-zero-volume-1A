# json_dumps.py - from Python values to JSON text
import json

payment = {"loan_id": "L00005", "amount": 194.73,
           "paid": True, "late_fee": None,
           "months": ["2025-01", "2025-02"]}

print(json.dumps(payment))
print(json.dumps(payment, indent=2))
