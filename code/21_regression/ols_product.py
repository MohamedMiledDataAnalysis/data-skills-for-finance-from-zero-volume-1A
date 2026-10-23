# ols_product.py - add the product as a categorical variable
import statsmodels.formula.api as smf

from regdata import load_loans, split, coef_table

train, test = split(load_loans())
print(train["product"].value_counts().sort_index())
simple = smf.ols("interest_rate ~ risk_rating",
                 data=train).fit()
model = smf.ols("interest_rate ~ risk_rating + C(product)",
                data=train).fit()
print(coef_table(model).round(4))
print(f"R-squared, rating only:      {simple.rsquared:.3f}")
print(f"R-squared, rating + product: {model.rsquared:.3f}")
print(f"Adjusted R-squared:          {model.rsquared_adj:.3f}")
