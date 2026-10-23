# new_columns.py - calculated columns
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")

loans["annual_interest"] = (
    loans["principal"] * loans["interest_rate"] / 100
).round(2)
loans["in_arrears"] = loans["status"] != "Performing"
loans["term_years"] = loans["term_months"] / 12

loans.loc[loans["principal"] >= 250000, "size_band"] = "Large"
loans.loc[loans["principal"] < 250000, "size_band"] = "Standard"

cols = ["loan_id", "principal", "interest_rate",
        "annual_interest", "in_arrears", "size_band"]
print(loans[cols].head())
total = loans["annual_interest"].sum()
print(f"Total annual interest: £{total:,.2f}")
print(loans["in_arrears"].sum())
