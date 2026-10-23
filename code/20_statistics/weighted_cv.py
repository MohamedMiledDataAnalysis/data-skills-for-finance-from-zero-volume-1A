# weighted_cv.py - weighted mean, coefficient of variation, NaN
import numpy as np
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")
rate, p = loans["interest_rate"], loans["principal"]

print(round(rate.mean(), 4))
print(round(np.average(rate, weights=p), 4))
print(round((rate * p).sum() / p.sum(), 4))

cv = p.std() / p.mean()
print(round(cv, 2))

ltv = loans["ltv"]
print(ltv.isna().sum(), ltv.count())
print(round(ltv.mean(), 2))
print(np.mean(ltv.to_numpy()))
