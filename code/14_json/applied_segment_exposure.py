# applied_segment_exposure.py - deposits by segment, in pounds
import json
from pathlib import Path

import pandas as pd

pd.options.display.float_format = "{:,.2f}".format

# 1. Extract the nested customer file, one row per account
with open("data/json/customers.json", encoding="utf-8") as f:
    customers = json.load(f)
accounts = pd.json_normalize(
    customers,
    record_path="accounts",
    meta=["customer_id", "segment", ["address", "country"]],
)
deposits = accounts[accounts["account_type"]
                    .isin(["Current", "Savings"])].copy()
print(len(accounts), "accounts,", len(deposits), "deposits")

# 2. Convert every balance to pounds with the last 2025 rate
fx = pd.read_csv("data/csv/fx_rates.csv")
last = fx[fx["rate_date"] == fx["rate_date"].max()]
rates = dict(zip(last["currency"], last["rate_per_gbp"]))
rates["GBP"] = 1.0
print("Rates used:", last["rate_date"].iloc[0], rates)
deposits["balance_gbp"] = (deposits["balance"]
                           / deposits["currency"].map(rates))

# 3. Summarise deposits by segment
summary = (deposits.groupby("segment")
           .agg(customers=("customer_id", "nunique"),
                accounts=("account_id", "count"),
                balance_gbp=("balance_gbp", "sum"))
           .reset_index())
summary["balance_gbp"] = summary["balance_gbp"].round(2)
summary["share_pct"] = (100 * summary["balance_gbp"]
                        / summary["balance_gbp"].sum()).round(2)
print(summary)

# 4. Write the result as JSON records for the next system
Path("output").mkdir(exist_ok=True)
summary.to_json("output/segment_exposure.json",
                orient="records", indent=2,
                double_precision=2)
print(Path("output/segment_exposure.json").read_text())
