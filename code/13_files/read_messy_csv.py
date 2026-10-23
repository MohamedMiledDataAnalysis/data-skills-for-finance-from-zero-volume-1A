# read_messy_csv.py - read the European file correctly
import pandas as pd

loans = pd.read_csv(
    "output/loans_eu.csv",
    encoding="cp1252",
    skiprows=1,
    sep=";",
    decimal=",",
    thousands=".",
    dtype={"loan_id": "str"},
    parse_dates=["origination_date"],
    dayfirst=True,
)
print(loans)
print(loans.dtypes)
print(f"Total principal: £{loans['principal'].sum():,.2f}")
