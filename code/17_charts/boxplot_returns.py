import matplotlib.pyplot as plt
import pandas as pd

from nbcharts import nb_style, add_titles, save_chart, PALETTE

nb_style()

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
wide = prices.pivot(index="price_date", columns="ticker",
                    values="close")
returns = wide.pct_change().dropna() * 100
tickers = ["NBB", "ATLS", "GRNE", "MERC"]
print(returns[tickers].std().round(2))

fig, ax = plt.subplots(figsize=(6, 3.4))
ax.boxplot([returns[t] for t in tickers], tick_labels=tickers,
           widths=0.5, patch_artist=True,
           boxprops={"facecolor": PALETTE["sand"],
                     "edgecolor": PALETTE["navy"]},
           medianprops={"color": PALETTE["navy"],
                        "linewidth": 2},
           whiskerprops={"color": PALETTE["navy"]},
           capprops={"color": PALETTE["navy"]},
           flierprops={"marker": "o", "markersize": 3,
                       "markerfacecolor": PALETTE["slate"],
                       "markeredgecolor": "white"})
ax.axhline(0, color="#9AA3B2", linewidth=0.8)
ax.set_xlabel("Share")
ax.set_ylabel("Daily return (%)")
ax.yaxis.set_major_formatter("{x:.0f}%")
ax.grid(axis="x", visible=False)
add_titles(ax, "Daily share price returns, 2025")
save_chart(fig, "ch17_boxplot_returns.png",
           "ch17-boxplot-returns.png")
