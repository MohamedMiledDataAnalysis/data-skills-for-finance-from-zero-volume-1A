# rolling.py - rolling 20-day mean and volatility of NBB
import numpy as np
import pandas as pd

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
nbb = (prices[prices["ticker"] == "NBB"]
       .set_index("price_date").sort_index())
nbb["ret"] = nbb["close"].pct_change()
nbb["ma20"] = nbb["close"].rolling(20).mean()
nbb["vol20"] = nbb["ret"].rolling(20).std() * np.sqrt(261)

print(nbb[["close", "ma20", "vol20"]].iloc[19:22].round(4))
print(round(nbb["vol20"].min(), 4), round(nbb["vol20"].max(), 4))
