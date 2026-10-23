# ex3_rate_in_logit.py - Exercise 3: add the rate to the logit
import statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score

from regdata import load_loans, split, coef_table

train, test = split(load_loans())
formulas = {
    "rating + product": "non_performing ~ risk_rating"
                        " + C(product)",
    "+ interest_rate": "non_performing ~ risk_rating"
                       " + C(product) + interest_rate"}
for name, formula in formulas.items():
    m = smf.logit(formula, data=train).fit(disp=0)
    auc = roc_auc_score(test["non_performing"], m.predict(test))
    print(f"{name}: test AUC {auc:.3f}")
print(coef_table(m)[["coef", "p_value"]].round(3))
rate = smf.ols("interest_rate ~ risk_rating + C(product)",
               data=train).fit()
print(f"R-squared, rate on rating + product: {rate.rsquared:.3f}")
