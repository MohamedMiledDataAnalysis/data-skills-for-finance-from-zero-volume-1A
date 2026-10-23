import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter, MonthLocator

from nbcharts import nb_style, add_titles, save_chart, PALETTE

nb_style()

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
nbb = prices[prices["ticker"] == "NBB"].set_index("price_date")
nbb = nbb.sort_index()
nbb["ma20"] = nbb["close"].rolling(20).mean()
print(nbb[["close", "ma20"]].tail(3).round(2))

fig, ax = plt.subplots(figsize=(6, 3.4))
ax.plot(nbb.index, nbb["close"], color=PALETTE["slate"],
        linewidth=1, label="Daily close")
ax.plot(nbb.index, nbb["ma20"], color=PALETTE["navy"],
        linewidth=1.8, label="20-day average")
ax.yaxis.set_major_formatter("£{x:.0f}")
ax.set_ylabel("Share price (£)")
ax.xaxis.set_major_locator(MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))
ax.legend(loc="upper left", ncols=2)
add_titles(ax, "NBB share price and 20-day moving average")
save_chart(fig, "ch17_ex2_rolling.png", "ch17-ex2.png")
