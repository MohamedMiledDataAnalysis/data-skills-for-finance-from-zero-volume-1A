# read_loans_options.py - read_csv options for finance files
import pandas as pd

loans = pd.read_csv(
    "data/csv/loans.csv",
    usecols=["loan_id", "customer_id", "product",
             "principal", "origination_date", "status"],
    dtype={"loan_id": "str", "customer_id": "str"},
    parse_dates=["origination_date"],
    nrows=5,
)
print(loans)
print(loans.dtypes)
