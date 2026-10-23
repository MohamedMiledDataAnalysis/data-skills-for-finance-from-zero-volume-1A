# straight_line.py - why a straight line fails for a yes/no target
import pandas as pd
import statsmodels.formula.api as smf

from regdata import load_loans, split

train, test = split(load_loans())
line = smf.ols("non_performing ~ risk_rating", data=train).fit()
print(line.params.round(4))
ratings = pd.DataFrame({"risk_rating": [1, 3, 5, 30]})
ratings["straight_line"] = line.predict(ratings)
print(ratings.round(4).to_string(index=False))
