# residuals.py - check the rate model through its residuals
import statsmodels.formula.api as smf

from regdata import load_loans, split

train, test = split(load_loans())
model = smf.ols("interest_rate ~ risk_rating + C(product)",
                data=train).fit()
train["fitted"] = model.fittedvalues
train["residual"] = train["interest_rate"] - train["fitted"]
cols = ["loan_id", "product", "risk_rating", "interest_rate",
        "fitted", "residual"]
print(train[cols].head(4).round(3).to_string(index=False))
print(train["residual"].describe().round(3))
print("Same as model.resid:",
      (train["residual"] - model.resid).abs().max() < 1e-9)
