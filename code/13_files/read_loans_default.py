# read_loans_default.py - what pandas guesses on its own
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")
print(loans.dtypes)
