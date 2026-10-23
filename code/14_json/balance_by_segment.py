# balance_by_segment.py - balances by segment and currency
import json

import pandas as pd

pd.options.display.float_format = "{:,.2f}".format

with open("data/json/customers.json", encoding="utf-8") as f:
    customers = json.load(f)

accounts = pd.json_normalize(
    customers,
    record_path="accounts",
    meta=["customer_id", "segment", ["address", "city"]],
)

by_segment = (accounts.groupby(["segment", "currency"])
              ["balance"].sum()
              .unstack("currency"))
print(by_segment)

print(accounts.groupby("segment")
      .agg(accounts=("account_id", "count"),
           customers=("customer_id", "nunique")))
