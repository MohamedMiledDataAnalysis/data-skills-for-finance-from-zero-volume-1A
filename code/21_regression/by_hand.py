# by_hand.py - slope and intercept of the line with two formulas
from regdata import load_loans, split

train, test = split(load_loans())
x = train["risk_rating"]
y = train["interest_rate"]

slope = x.cov(y) / x.var()
intercept = y.mean() - slope * x.mean()
print(f"Mean rating {x.mean():.4f}, mean rate {y.mean():.4f}")
print(f"Slope b = {slope:.4f}")
print(f"Intercept a = {intercept:.4f}")
print(f"Rating 4: {intercept + slope * 4:.2f}%")
