# mode_rating.py - the most common customer risk rating
import pandas as pd

customers = pd.read_csv("data/csv/customers.csv")
rating = customers["risk_rating"]

print(rating.value_counts().sort_index())
print(rating.mode())
print(rating.value_counts().idxmax())
