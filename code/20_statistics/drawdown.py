# drawdown.py - running peak and maximum drawdown
import sys
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import nb_style, add_titles, save_chart, PALETTE

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
prices = prices.sort_values(["ticker", "price_date"])
prices["peak"] = prices.groupby("ticker")["close"].cummax()
prices["drawdown"] = prices["close"] / prices["peak"] - 1

worst = prices.loc[prices.groupby("ticker")["drawdown"].idxmin()]
worst = worst.assign(max_dd=(100 * worst["drawdown"]).round(2))
print(worst[["ticker", "max_dd", "price_date"]]
      .to_string(index=False))

nbb = prices[prices["ticker"] == "NBB"]
low = nbb.loc[nbb["drawdown"].idxmin()]

nb_style()
fig, ax = plt.subplots()
dd = 100 * nbb["drawdown"]
ax.fill_between(nbb["price_date"], dd, 0, color=PALETTE["red"],
                alpha=0.25, linewidth=0)
ax.plot(nbb["price_date"], dd, color=PALETTE["red"],
        linewidth=1)
ax.annotate(f"Maximum drawdown {100 * low['drawdown']:.1f}%",
            xy=(low["price_date"], 100 * low["drawdown"]),
            xytext=(-12, -4), textcoords="offset points",
            ha="right", va="top", fontsize=8, color="#333333")
ax.set_ylim(100 * low["drawdown"] * 1.25, 1)
ax.set_xlim(nbb["price_date"].min(), nbb["price_date"].max())
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.yaxis.set_major_formatter("{x:.0f}%")
ax.set_ylabel("Drawdown from previous peak (%)")
add_titles(ax, "How far NBB stood below its previous peak")
save_chart(fig, "ch20_nbb_drawdown.png", "ch20-nbb-drawdown.png")
