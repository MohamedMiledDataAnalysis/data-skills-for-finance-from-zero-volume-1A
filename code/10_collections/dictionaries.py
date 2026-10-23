# dictionaries.py - values looked up by name
loan = {
    "loan_id": "L00001",
    "product": "SME",
    "principal": 297735.46,
    "interest_rate": 7.81,
    "status": "90+ DPD",
}

print(loan["product"])
print(loan["principal"])

loan["status"] = "Default"          # change a value
loan["sector"] = "Construction"     # add a new key
print(loan["status"], loan["sector"], len(loan))

print(loan.keys())
print(loan.values())
print(loan.get("ltv"))              # missing key: None
print(loan.get("ltv", "n/a"))       # missing key: default
print("ltv" in loan)
