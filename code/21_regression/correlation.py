# correlation.py - how closely rate and risk rating move together
from regdata import load_loans, split

train, test = split(load_loans())
pair = train[["interest_rate", "risk_rating"]]
print(pair.corr().round(3))
r = train["interest_rate"].corr(train["risk_rating"])
print(f"Correlation on the training set: {r:.3f}")
by_product = train.groupby("product")[pair.columns].apply(
    lambda g: g["interest_rate"].corr(g["risk_rating"]))
print(by_product.round(3))
