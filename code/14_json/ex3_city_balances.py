# ex3_city_balances.py - Exercise 3, sterling balances by city
import json

import pandas as pd

pd.options.display.float_format = "{:,.2f}".format

with open("data/json/customers.json", encoding="utf-8") as f:
    customers = json.load(f)

accounts = pd.json_normalize(
    customers,
    record_path="accounts",
    meta=["customer_id", ["address", "city"]],
)
gbp = accounts[accounts["currency"] == "GBP"]
top = (gbp.groupby("address.city")["balance"].sum()
       .sort_values(ascending=False))
print(top)
