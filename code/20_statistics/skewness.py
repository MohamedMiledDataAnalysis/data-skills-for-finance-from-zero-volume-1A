# skewness.py - skewness of loan principal, pandas and by formula
import numpy as np
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")
p = loans["principal"]
five = pd.Series([12, 15, 18, 25, 80])


def moment_skew(x):
    """Average cubed z-score: the textbook (moment) skewness."""
    z = (x - x.mean()) / x.std(ddof=0)
    return (z ** 3).mean()


print(round(five.skew(), 4), round(moment_skew(five), 4))
print(round(p.skew(), 4), round(moment_skew(p), 4))
print(round(np.log(p).skew(), 4))
print(loans.groupby("product")["principal"].skew().round(3))
