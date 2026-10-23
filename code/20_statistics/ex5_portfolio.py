# ex5_portfolio.py - Exercise 5: equal-weight portfolio
import numpy as np
import pandas as pd

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
wide = prices.pivot(index="price_date", columns="ticker",
                    values="close")
returns = wide.pct_change().dropna()

weights = pd.Series(0.25, index=returns.columns)
port = returns @ weights            # daily portfolio return
print(port.head(3).round(5))


def ann_vol(r):
    return r.std() * np.sqrt(261)


single = ann_vol(returns)           # one value per share
print((100 * single).round(2))
avg_single = single.mean()
print(f"Average single-share volatility: {100 * avg_single:.2f}%")
print(f"Portfolio volatility:            "
      f"{100 * ann_vol(port):.2f}%")
cut = 1 - ann_vol(port) / avg_single
print(f"Reduction: {100 * cut:.1f}%")
total = (1 + port).prod() - 1
print(f"Portfolio 2025 return: {100 * total:.1f}%")
