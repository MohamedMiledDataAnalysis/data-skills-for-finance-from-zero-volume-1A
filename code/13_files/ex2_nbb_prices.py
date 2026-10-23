# ex2_nbb_prices.py - Exercise 2, the NBB share price
import pandas as pd

prices = pd.read_excel(
    "data/excel/northbridge.xlsx",
    sheet_name="market_prices",
    parse_dates=["price_date"],
)
nbb = prices[prices["ticker"] == "NBB"]
print("Trading days:", len(nbb))
print("Lowest close:", nbb["close"].min())
print("Highest close:", nbb["close"].max())
low_day = nbb.loc[nbb["close"].idxmin(), "price_date"]
print("Lowest on:", low_day.date())
