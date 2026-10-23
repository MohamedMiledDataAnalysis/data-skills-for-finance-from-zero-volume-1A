# ex5_risk_bands.py - Exercise 5: a risk-band (gains) table
import pandas as pd
import statsmodels.formula.api as smf

from regdata import load_loans, split

train, test = split(load_loans())
model = smf.logit("non_performing ~ risk_rating + C(product)",
                  data=train).fit(disp=0)
test["prob"] = model.predict(test)
order = test["prob"].rank(method="first", ascending=False)
test["band"] = pd.qcut(order, 5, labels=[1, 2, 3, 4, 5])

bands = test.groupby("band", observed=True).agg(
    loans=("loan_id", "count"),
    p_min=("prob", "min"),
    p_max=("prob", "max"),
    predicted=("prob", "mean"),
    non_perf=("non_performing", "sum"),
    actual=("non_performing", "mean"))
bands["caught"] = (bands["non_perf"].cumsum()
                         / bands["non_perf"].sum())
pcts = ["p_min", "p_max", "predicted", "actual", "caught"]
bands[pcts] = bands[pcts] * 100
print(bands.round(1).to_string())
