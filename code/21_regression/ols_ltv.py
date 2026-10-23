# ols_ltv.py - does LTV explain the rate of a mortgage?
import statsmodels.formula.api as smf

from regdata import load_loans, split, coef_table

train, test = split(load_loans())
mortgages = train[train["product"] == "Mortgage"]
model = smf.ols("interest_rate ~ risk_rating + ltv",
                data=mortgages).fit()
print(f"Mortgages in the training set: {model.nobs:.0f}")
print(coef_table(model).round(4))
change = model.params["ltv"] * 10
print(f"Effect of 10 more LTV points: {change:.3f} pp")
