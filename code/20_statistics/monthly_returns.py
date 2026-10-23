# monthly_returns.py - monthly returns of NBB, coloured by sign
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import nb_style, add_titles, save_chart, PALETTE

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
nbb = (prices[prices["ticker"] == "NBB"]
       .set_index("price_date").sort_index())

month_end = nbb["close"].resample("ME").last()
monthly = month_end.to_frame()
monthly["ret_pct"] = 100 * month_end.pct_change()
print(monthly.round(2).head(3))
print("...")
print(monthly.round(2).tail(1))

data = monthly.dropna()
colours = [PALETTE["teal"] if r >= 0 else PALETTE["red"]
           for r in data["ret_pct"]]
nb_style()
fig, ax = plt.subplots()
ax.bar(data.index.strftime("%b"), data["ret_pct"],
       color=colours, width=0.7)
ax.axhline(0, color=PALETTE["slate"], linewidth=0.8)
ax.yaxis.set_major_locator(MultipleLocator(2))
ax.yaxis.set_major_formatter("{x:.0f}%")
ax.set_xlabel("Month ending")
ax.set_ylabel("Monthly return (%)")
ax.grid(axis="x", visible=False)
add_titles(ax, "NBB monthly returns in 2025: teal gains, "
               "red losses")
save_chart(fig, "ch20_nbb_monthly.png", "ch20-nbb-monthly.png")
