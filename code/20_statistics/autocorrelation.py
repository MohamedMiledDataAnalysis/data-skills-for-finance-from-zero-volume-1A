# autocorrelation.py - autocorrelation of prices and returns
import numpy as np
import pandas as pd

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
wide = prices.pivot(index="price_date", columns="ticker",
                    values="close")
returns = wide.pct_change().dropna()

lags = range(1, 6)
acf = pd.DataFrame({
    "price": [wide["NBB"].autocorr(lag=k) for k in lags],
    "return": [returns["NBB"].autocorr(lag=k) for k in lags],
}, index=pd.Index(lags, name="lag"))
print(acf.round(3))
print(round(2 / np.sqrt(len(returns)), 4))

print(returns.corr().round(2))
