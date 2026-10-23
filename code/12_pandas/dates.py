# dates.py - parse dates and group by year
import pandas as pd

loans = pd.read_csv(
    "data/csv/loans.csv", parse_dates=["origination_date"]
)
print(loans["origination_date"].dtype)
print(loans["origination_date"].min())
print(loans["origination_date"].max())

loans["orig_year"] = loans["origination_date"].dt.year
vintages = loans.groupby("orig_year").agg(
    loans=("loan_id", "count"),
    principal=("principal", "sum"),
)
print(vintages.round(0))

reporting = pd.Timestamp("2025-12-31")
age = reporting - loans["origination_date"]
loans["days_on_book"] = age.dt.days
cols = ["loan_id", "origination_date", "days_on_book"]
print(loans[cols].head(3))
