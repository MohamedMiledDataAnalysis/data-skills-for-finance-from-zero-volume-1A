# json_load_file.py - read a JSON file with the json module
import json

with open("data/json/loans.json", encoding="utf-8") as f:
    loans = json.load(f)

print(type(loans).__name__, len(loans))
first = loans[0]
print(first["loan_id"], first["product"], first["principal"])

mortgages = [x for x in loans if x["product"] == "Mortgage"]
total = sum(x["principal"] for x in mortgages)
print(f"{len(mortgages)} mortgages, £{total:,.2f}")
