# outliers_iqr.py - the 1.5 x IQR rule on loan principal
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")
p = loans["principal"]

q1, q3 = p.quantile(0.25), p.quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
print(f"Fences: {lower:,.2f} and {upper:,.2f}")

big = loans[p > upper]
print(len(big))
print(big["product"].value_counts())
