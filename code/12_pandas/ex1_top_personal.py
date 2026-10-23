# ex1_top_personal.py - Exercise 1: five largest personal loans
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")

personal = loans[loans["product"] == "Personal"]
top5 = personal.sort_values("principal", ascending=False).head(5)
print(top5[["loan_id", "principal", "interest_rate", "status"]])
print(f"Personal loans: {len(personal)}")
