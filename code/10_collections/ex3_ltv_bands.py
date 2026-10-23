# ex3_ltv_bands.py - Exercise 3: mortgages by LTV band
import csv

bands = {"Up to 60%": 0, "60-80%": 0, "Over 80%": 0}

with open("data/csv/loans.csv", newline="") as f:
    for row in csv.DictReader(f):
        if row["product"] != "Mortgage":
            continue
        ltv = float(row["ltv"])
        if ltv <= 60:
            bands["Up to 60%"] += 1
        elif ltv <= 80:
            bands["60-80%"] += 1
        else:
            bands["Over 80%"] += 1

for band, n in bands.items():
    print(f"{band:<10} {n:>4}")
print(f"{'Total':<10} {sum(bands.values()):>4}")
