# ex4_split_combine_loans.py - Exercise 4, split and recombine
from pathlib import Path

import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")
folder = Path("output/loans_by_product")
folder.mkdir(parents=True, exist_ok=True)
for product, part in loans.groupby("product"):
    part.to_csv(folder / f"loans_{product}.csv", index=False)

paths = sorted(folder.glob("loans_*.csv"))
combined = pd.concat([pd.read_csv(p) for p in paths],
                     ignore_index=True)

print([p.name for p in paths])
print("Rows:", len(combined))
print(f"Principal: {combined['principal'].sum():,.2f}")
assert len(combined) == len(loans) == 1200
assert round(combined["principal"].sum(), 2) == round(
    loans["principal"].sum(), 2)
print("Both checks passed")
