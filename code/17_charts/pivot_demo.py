import pandas as pd

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
print(prices.head(4))
wide = prices.pivot(index="price_date", columns="ticker",
                    values="close")
print(wide.head(2))
print("Long:", prices.shape, "| wide:", wide.shape)
