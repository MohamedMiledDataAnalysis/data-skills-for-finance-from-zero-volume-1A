# normal_var.py - returns against the normal curve, and VaR
import sys
from pathlib import Path
from statistics import NormalDist

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import nb_style, add_titles, save_chart, PALETTE

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
nbb = (prices[prices["ticker"] == "NBB"]
       .set_index("price_date").sort_index())
ret = nbb["close"].pct_change().dropna()

m, s = ret.mean(), ret.std()
print(round(m, 5), round(s, 5))
for k in (1, 2, 3):
    share = ((ret - m).abs() <= k * s).mean()
    print(k, round(100 * share, 1))

z = NormalDist().inv_cdf(0.05)     # 5th percentile of N(0, 1)
print(round(z, 4))

POSITION = 1_000_000               # £1m held in NBB shares
q05 = ret.quantile(0.05)
var_hist = -q05 * POSITION
var_norm = -(m + z * s) * POSITION
print(f"Historical VaR: £{var_hist:,.0f}")
print(f"Normal VaR:     £{var_norm:,.0f}")
print((ret <= q05).sum())

nb_style()
fig, ax = plt.subplots()
bins = np.arange(-0.044, 0.056, 0.004)
ax.hist(100 * ret, bins=100 * bins, density=True,
        color=PALETTE["teal"], edgecolor="white", linewidth=0.4)
xs = np.linspace(-0.05, 0.06, 300)
curve = [NormalDist(m, s).pdf(x) / 100 for x in xs]
ax.plot(100 * xs, curve, color=PALETTE["navy"], linewidth=1.6,
        label="Normal curve, same mean and sd")
ax.axvline(100 * q05, color=PALETTE["red"], linewidth=1.2)
ax.text(100 * q05 - 0.15, 0.97, "5th percentile", ha="right",
        va="top", transform=ax.get_xaxis_transform(),
        fontsize=8, color="#333333")
ax.xaxis.set_major_formatter("{x:.0f}%")
ax.set_xlabel("Daily return (%)")
ax.set_ylabel("Density (share of days per 1%)")
ax.legend(loc="upper right")
add_titles(ax, "NBB daily returns follow the normal curve")
save_chart(fig, "ch20_returns_normal.png",
           "ch20-returns-normal.png")
