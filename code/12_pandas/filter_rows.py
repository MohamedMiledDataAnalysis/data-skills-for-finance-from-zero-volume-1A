# filter_rows.py - keep the rows that meet a condition
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")

is_default = loans["status"] == "Default"
print(is_default.head())
print(is_default.sum())

defaults = loans[is_default]
print(defaults.shape)

big_mortgages = loans[
    (loans["product"] == "Mortgage") & (loans["principal"] > 500000)
]
print(len(big_mortgages))

in_arrears = loans[loans["status"].isin(["30+ DPD", "90+ DPD"])]
print(len(in_arrears))

risky = loans[(loans["status"] == "Default") | (loans["ltv"] > 90)]
print(len(risky))

mid_rate = loans[loans["interest_rate"].between(5, 6)]
print(len(mid_rate))

cols = ["loan_id", "principal", "interest_rate", "status"]
print(loans.loc[loans["product"] == "Auto", cols].head(3))
