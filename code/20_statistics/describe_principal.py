# describe_principal.py - descriptive statistics of loan principal
import numpy as np
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")
p = loans["principal"]

print(round(p.mean(), 2), round(p.median(), 2))
print(p.min(), p.max())
print(round(p.var()), round(p.std(), 2))
print(p.quantile([0.05, 0.95]).round(2))
iqr = p.quantile(0.75) - p.quantile(0.25)
print(round(iqr, 2))
print(p.describe().round(2))

top20 = p.nlargest(20).sum() / p.sum()
print(round(100 * top20, 1))
print(np.quantile(p, 0.25, method="weibull").round(2))
