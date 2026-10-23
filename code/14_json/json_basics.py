# json_basics.py - from JSON text to Python values
import json

text = """
{
  "loan_id": "L00001",
  "principal": 297735.46,
  "term_months": 60,
  "secured": false,
  "ltv": null,
  "tags": ["SME", "watchlist"]
}
"""
loan = json.loads(text)
print(type(loan))
for key, value in loan.items():
    print(f"{key:<13}{type(value).__name__:<10}{value!r}")
