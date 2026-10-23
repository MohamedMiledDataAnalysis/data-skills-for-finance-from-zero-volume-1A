# ex3_messy_accounts.py - Exercise 3, a French accounts file
from pathlib import Path

import pandas as pd

accounts = pd.read_csv("data/csv/accounts.csv")

Path("output").mkdir(exist_ok=True)
with open("output/accounts_eu.csv", "w",
          encoding="cp1252") as f:
    f.write("Northbridge Bank – Comptes\n")
    f.write("Extraction du 31/12/2025\n")
    accounts.to_csv(f, sep=";", decimal=",", index=False)

back = pd.read_csv(
    "output/accounts_eu.csv",
    encoding="cp1252",
    skiprows=2,
    sep=";",
    decimal=",",
    dtype={"account_id": "str", "customer_id": "str"},
)
print(back.shape)
print(back.head(3))
print(f"Original total: {accounts['balance'].sum():,.2f}")
print(f"Read-back total: {back['balance'].sum():,.2f}")
