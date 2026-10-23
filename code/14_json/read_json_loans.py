# read_json_loans.py - flat JSON into pandas
import pandas as pd

pd.options.display.float_format = "{:,.2f}".format

loans = pd.read_json("data/json/loans.json",
                     dtype={"loan_id": "str"})
print(loans.shape)
print(loans.dtypes)
print(loans.head(3).iloc[:, :6])

print(loans.groupby("status")["principal"].sum())
