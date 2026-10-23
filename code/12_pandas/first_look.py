# first_look.py - load the loan book and inspect it
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")

print(loans.head())
print(loans.shape)
print(loans.columns)
print(loans.dtypes)
