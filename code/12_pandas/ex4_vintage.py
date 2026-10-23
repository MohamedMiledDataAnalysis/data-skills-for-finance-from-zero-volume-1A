# ex4_vintage.py - Exercise 4: arrears rate by origination year
import pandas as pd

loans = pd.read_csv(
    "data/csv/loans.csv", parse_dates=["origination_date"]
)
loans["year"] = loans["origination_date"].dt.year
loans["in_arrears"] = loans["status"] != "Performing"

vintage = loans.groupby("year").agg(
    loans=("loan_id", "count"),
    arrears=("in_arrears", "sum"),
    arrears_rate=("in_arrears", "mean"),
)
vintage["arrears_rate"] = (vintage["arrears_rate"] * 100).round(1)
print(vintage)
