# ex1_accounts_options.py - Exercise 1, read only what you need
import pandas as pd

accounts = pd.read_csv(
    "data/csv/accounts.csv",
    usecols=["account_id", "customer_id", "currency", "balance"],
    dtype={"account_id": "str", "customer_id": "str"},
    nrows=10,
)
print(accounts)
print(accounts.dtypes)
