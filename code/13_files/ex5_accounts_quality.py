# ex5_accounts_quality.py - Exercise 5, accounts quality workbook
from pathlib import Path

import pandas as pd

accounts = pd.read_excel(
    "data/excel/northbridge.xlsx",
    sheet_name="accounts",
    dtype={"account_id": "str", "customer_id": "str"},
)
allowed = {"GBP", "EUR", "USD"}
overdrawn = accounts[accounts["balance"] < 0]

checks = pd.DataFrame({
    "check": ["rows", "duplicate account_id",
              "missing values", "unknown currency",
              "overdrawn accounts"],
    "value": [len(accounts),
              accounts["account_id"].duplicated().sum(),
              accounts.isna().sum().sum(),
              (~accounts["currency"].isin(allowed)).sum(),
              len(overdrawn)],
})
print(checks)
print(overdrawn.groupby("currency")["balance"].sum())

Path("output").mkdir(exist_ok=True)
with pd.ExcelWriter("output/accounts_quality.xlsx") as writer:
    checks.to_excel(writer, sheet_name="checks", index=False)
    overdrawn.to_excel(writer, sheet_name="overdrawn",
                       index=False)
print(pd.read_excel("output/accounts_quality.xlsx",
                    sheet_name=None).keys())
