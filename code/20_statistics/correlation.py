# correlation.py - covariance and correlation of loan fields
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")
p, rate = loans["principal"], loans["interest_rate"]

print(round(p.cov(rate), 1))
print(round(p.corr(rate), 4))
print(round(p.corr(rate, method="spearman"), 4))

num = loans[["principal", "interest_rate", "term_months", "ltv"]]
print(num.corr().round(2))
