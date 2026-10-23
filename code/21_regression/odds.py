# odds.py - probability, odds and log-odds by risk rating
import numpy as np

from regdata import load_loans, split

train, test = split(load_loans())
table = train.groupby("risk_rating")["non_performing"].agg(
    loans="count", non_perf="sum", probability="mean")
table["odds"] = table["probability"] / (1 - table["probability"])
table["log_odds"] = np.log(table["odds"])
print(table.round(3))
