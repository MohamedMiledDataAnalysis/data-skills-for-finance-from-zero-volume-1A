# logit_fit.py - a logistic model of non-performing loans
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from regdata import load_loans, split, coef_table

train, test = split(load_loans())
model = smf.logit("non_performing ~ risk_rating + C(product)",
                  data=train).fit()
print(coef_table(model).round(4))

ratios = np.exp(coef_table(model)[["coef", "ci_low",
                                   "ci_high"]])
ratios.columns = ["odds_ratio", "ci_low", "ci_high"]
print(ratios.round(3))

grid = pd.DataFrame({
    "risk_rating": [1, 2, 3, 4, 5] * 2,
    "product": ["Personal"] * 5 + ["Mortgage"] * 5})
grid["probability"] = model.predict(grid)
print(grid.pivot(index="risk_rating", columns="product",
                 values="probability").mul(100).round(2))
