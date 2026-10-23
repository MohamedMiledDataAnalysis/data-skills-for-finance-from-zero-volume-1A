# split_by_month.py - one CSV file per month
from pathlib import Path

import pandas as pd

txns = pd.read_csv("data/csv/transactions.csv")
txns["month"] = txns["txn_date"].str[:7]

folder = Path("output/transactions_by_month")
folder.mkdir(parents=True, exist_ok=True)

for month, part in txns.groupby("month"):
    path = folder / f"transactions_{month}.csv"
    part.drop(columns="month").to_csv(path, index=False)
    print(path, len(part))
