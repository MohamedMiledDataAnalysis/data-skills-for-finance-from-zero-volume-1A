# ex2_new_loans.py - Exercise 2: quote rates for three new loans
import pandas as pd
import statsmodels.formula.api as smf

from regdata import load_loans, split

train, test = split(load_loans())
model = smf.ols("interest_rate ~ risk_rating + C(product)",
                data=train).fit()
new = pd.DataFrame({
    "applicant": ["A", "B", "C"],
    "product": ["Mortgage", "Auto", "SME"],
    "risk_rating": [2, 5, 3]})
pred = model.get_prediction(new).summary_frame(alpha=0.05)
new["rate"] = pred["mean"]
new["low"] = pred["obs_ci_lower"]
new["high"] = pred["obs_ci_upper"]
print(new.round(2).to_string(index=False))
