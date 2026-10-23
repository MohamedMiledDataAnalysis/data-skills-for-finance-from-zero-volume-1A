# sort_rows.py - sort by one or more columns
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")
cols = ["loan_id", "product", "principal", "status"]

largest = loans.sort_values("principal", ascending=False)
print(largest[cols].head(5))

by_two = loans.sort_values(
    ["product", "interest_rate"], ascending=[True, False]
)
print(by_two[["loan_id", "product", "interest_rate"]].head(3))

print(loans.nlargest(3, "interest_rate")[
    ["loan_id", "product", "interest_rate"]
])
