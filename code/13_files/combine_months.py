# combine_months.py - combine monthly files and check rows
from pathlib import Path

import pandas as pd

folder = Path("output/transactions_by_month")
paths = sorted(folder.glob("transactions_*.csv"))
print("Files found:", len(paths))

parts = []
for path in paths:
    part = pd.read_csv(path, dtype={"account_id": "str"})
    part["source_file"] = path.name
    parts.append(part)

txns = pd.concat(parts, ignore_index=True)
print("Rows combined:", len(txns))

original = pd.read_csv("data/csv/transactions.csv")
assert len(txns) == len(original) == 20_000
print("Check passed: row count matches the original file")
print(txns.groupby("source_file").size().head(3))
