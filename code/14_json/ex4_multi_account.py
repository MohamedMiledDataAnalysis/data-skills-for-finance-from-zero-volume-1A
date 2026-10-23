# ex4_multi_account.py - Exercise 4, accounts per customer
import json

import pandas as pd

with open("data/json/customers.json", encoding="utf-8") as f:
    customers = json.load(f)

people = pd.json_normalize(customers)
people["n_accounts"] = people["accounts"].apply(len)
print(people["n_accounts"].value_counts().sort_index())

three = people[people["n_accounts"] == 3]
print(three[["customer_id", "segment",
             "address.city"]].head(5))
