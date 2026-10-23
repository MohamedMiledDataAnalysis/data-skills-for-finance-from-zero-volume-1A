# info_describe.py - structure and summary statistics
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")

loans.info()
print(loans.describe().round(2))
