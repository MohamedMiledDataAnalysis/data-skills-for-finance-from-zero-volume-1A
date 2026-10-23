# ex1_segment.py - Exercise 1: does the segment improve the model?
import statsmodels.formula.api as smf

from regdata import load_loans, split, coef_table

train, test = split(load_loans())
base = smf.ols("interest_rate ~ risk_rating + C(product)",
               data=train).fit()
seg = smf.ols("interest_rate ~ risk_rating + C(product)"
              " + C(segment)", data=train).fit()
print(coef_table(seg)[["coef", "p_value"]].round(4))
for name, m in [("Without segment", base),
                ("With segment", seg)]:
    print(f"{name}: R2 {m.rsquared:.4f}, "
          f"adjusted R2 {m.rsquared_adj:.4f}")
