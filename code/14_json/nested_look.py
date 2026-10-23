# nested_look.py - look inside nested JSON
import json

import pandas as pd

with open("data/json/customers.json", encoding="utf-8") as f:
    customers = json.load(f)

c = customers[4]
print(json.dumps(c, indent=2))
print(c["address"]["city"])
print(c["accounts"][0]["balance"])

flat = pd.DataFrame(customers)
print(flat[["customer_id", "address"]].head(2))
