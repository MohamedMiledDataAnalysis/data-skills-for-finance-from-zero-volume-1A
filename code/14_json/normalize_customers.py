# normalize_customers.py - flatten nested JSON
import json

import pandas as pd

with open("data/json/customers.json", encoding="utf-8") as f:
    customers = json.load(f)

top = pd.json_normalize(customers)
print(top.columns.tolist())

accounts = pd.json_normalize(
    customers,
    record_path="accounts",
    meta=["customer_id", "first_name", "last_name", "segment",
          ["address", "city"], ["address", "country"]],
)
print(accounts.shape)
print(accounts.columns.tolist())
cols = ["account_id", "currency", "balance",
        "customer_id", "segment", "address.city"]
print(accounts[cols].head(4))
