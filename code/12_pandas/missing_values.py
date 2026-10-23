# missing_values.py - NaN in the ltv column
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")

print(loans["ltv"].head())
print(loans.isna().sum())

no_ltv = loans.loc[loans["ltv"].isna(), "product"]
print(no_ltv.value_counts())

print(loans["ltv"].mean())

filled = loans["ltv"].fillna(0)
print(filled.mean())

mortgages = loans.dropna(subset=["ltv"])
print(mortgages.shape)
print(mortgages["product"].unique())
