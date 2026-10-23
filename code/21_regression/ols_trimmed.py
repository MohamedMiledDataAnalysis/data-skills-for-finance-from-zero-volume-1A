# ols_trimmed.py - the numbers a junior analyst reads first
import statsmodels.formula.api as smf

from regdata import load_loans, split, coef_table

train, test = split(load_loans())
model = smf.ols("interest_rate ~ risk_rating", data=train).fit()
print(model.params)
print(coef_table(model).round(4))
print(f"R-squared {model.rsquared:.3f}, n = {model.nobs:.0f}")
