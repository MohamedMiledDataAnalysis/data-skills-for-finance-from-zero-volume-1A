# ex5_overdrawn_json.py - Exercise 5, overdrawn accounts as JSON
import json
from pathlib import Path

import pandas as pd

with open("data/json/customers.json", encoding="utf-8") as f:
    customers = json.load(f)

accounts = pd.json_normalize(
    customers,
    record_path="accounts",
    meta=["customer_id", "first_name", "last_name",
          ["address", "country"]],
)
overdrawn = (accounts[accounts["balance"] < 0]
             .sort_values("balance")
             .rename(columns={"address.country": "country"}))
print(len(overdrawn), "overdrawn accounts")

Path("output").mkdir(exist_ok=True)
overdrawn.to_json("output/overdrawn_accounts.json",
                  orient="records", indent=2)

back = pd.read_json("output/overdrawn_accounts.json")
print(back.shape)
print(back[["account_id", "customer_id", "currency",
            "balance", "country"]].head(3))
text = Path("output/overdrawn_accounts.json").read_text()
print(text[:220])
