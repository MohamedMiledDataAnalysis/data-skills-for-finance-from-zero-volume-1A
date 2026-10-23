# returns.py - daily returns, cumulative and annualised figures
import numpy as np
import pandas as pd

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
prices = prices.sort_values(["ticker", "price_date"])
by_ticker = prices.groupby("ticker")["close"]
prices["ret"] = by_ticker.pct_change()
prices["log_ret"] = np.log(prices["close"] / by_ticker.shift(1))

cols = ["price_date", "close", "ret", "log_ret"]
print(prices.loc[prices["ticker"] == "NBB", cols].head(3))

RF = 0.04          # ASSUMPTION: risk-free rate, 4% a year
DAYS_YEAR = 261    # weekday rows per year in this file

rets = prices.dropna(subset=["ret"])
perf = rets.groupby("ticker").agg(
    days=("ret", "size"),
    cum_simple=("ret", lambda r: (1 + r).prod() - 1),
    cum_log=("log_ret", lambda r: np.exp(r.sum()) - 1),
    mean_daily=("ret", "mean"),
    sd_daily=("ret", "std"),
)
perf["ann_return"] = ((1 + perf["cum_simple"])
                      ** (DAYS_YEAR / perf["days"]) - 1)
perf["ann_vol"] = perf["sd_daily"] * np.sqrt(DAYS_YEAR)
perf["sharpe"] = (perf["ann_return"] - RF) / perf["ann_vol"]

print(perf["days"].tolist())
show = perf.drop(columns=["days", "sd_daily"])
pct_cols = ["cum_simple", "cum_log", "mean_daily",
            "ann_return", "ann_vol"]
show[pct_cols] = (100 * show[pct_cols]).round(3)
print(show.round({"sharpe": 2}))
