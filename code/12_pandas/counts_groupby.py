# counts_groupby.py - counting and summarising by group
import pandas as pd

pd.options.display.float_format = "{:,.2f}".format

loans = pd.read_csv("data/csv/loans.csv")

print(loans["status"].value_counts())
print(loans["status"].value_counts(normalize=True) * 100)

summary = loans.groupby("product").agg(
    loans=("loan_id", "count"),
    total_principal=("principal", "sum"),
    avg_principal=("principal", "mean"),
    avg_rate=("interest_rate", "mean"),
)
print(summary)

by_two = loans.groupby(["product", "status"]).agg(
    loans=("loan_id", "count"),
    principal=("principal", "sum"),
)
print(by_two.head(8))
