# ex2_terms.py - Exercise 2: mortgage terms
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")

mortgages = loans[loans["product"] == "Mortgage"]
print(mortgages["term_months"].value_counts().sort_index())
print((mortgages["term_months"] / 12).value_counts().sort_index())
