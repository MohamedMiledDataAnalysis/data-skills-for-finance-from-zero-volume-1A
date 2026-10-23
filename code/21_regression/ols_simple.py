# ols_simple.py - the same line with statsmodels
import statsmodels.formula.api as smf

from regdata import load_loans, split

train, test = split(load_loans())
model = smf.ols("interest_rate ~ risk_rating", data=train).fit()
for table in model.summary().tables[:2]:
    print(table)
