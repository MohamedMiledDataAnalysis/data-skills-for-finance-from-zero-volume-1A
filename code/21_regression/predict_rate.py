# predict_rate.py - test the rate model on loans it has not seen
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from regdata import load_loans, split

train, test = split(load_loans())
model = smf.ols("interest_rate ~ risk_rating + C(product)",
                data=train).fit()

test["predicted"] = model.predict(test)
error = test["interest_rate"] - test["predicted"]
rmse = np.sqrt((error ** 2).mean())
mae = error.abs().mean()
ss_res = (error ** 2).sum()
ss_tot = ((test["interest_rate"]
           - test["interest_rate"].mean()) ** 2).sum()
print(f"Test loans: {len(test)}")
print(f"RMSE: {rmse:.3f} pp")
print(f"MAE:  {mae:.3f} pp")
print(f"R-squared on test: {1 - ss_res / ss_tot:.3f}")
print(f"R-squared on training: {model.rsquared:.3f}")

new_loan = pd.DataFrame({"risk_rating": [4],
                         "product": ["Personal"]})
rate = model.predict(new_loan).iloc[0]
print(f"New Personal loan, rating 4: {rate:.2f}%")
