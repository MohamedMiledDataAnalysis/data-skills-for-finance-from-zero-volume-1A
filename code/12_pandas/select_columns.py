# select_columns.py - one column (Series) or several (DataFrame)
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")

principal = loans["principal"]
print(type(principal))
print(principal.head(3))
print(principal.sum(), principal.mean(), principal.max())

subset = loans[["loan_id", "product", "principal"]]
print(type(subset))
print(subset.head(3))
