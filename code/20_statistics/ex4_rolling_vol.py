# ex4_rolling_vol.py - Exercise 4: rolling 60-day volatility
import sys
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import nb_style, add_titles, save_chart, PALETTE

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
wide = prices.pivot(index="price_date", columns="ticker",
                    values="close")[["NBB", "MERC"]]
vol60 = (wide.pct_change().rolling(60).std()
         * np.sqrt(261) * 100).dropna()

print(vol60.index[0].date())
print(vol60.agg(["min", "max"]).round(1))

nb_style()
fig, ax = plt.subplots()
for ticker, colour in [("NBB", "navy"), ("MERC", "gold")]:
    ax.plot(vol60.index, vol60[ticker], color=PALETTE[colour],
            linewidth=1.8)
    ax.text(vol60.index[-1], vol60[ticker].iloc[-1],
            f"  {ticker}", va="center", fontsize=8,
            color="#333333")
ax.set_ylim(0, 30)
ax.set_xlim(vol60.index[0], vol60.index[-1] + pd.Timedelta(days=20))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.yaxis.set_major_formatter("{x:.0f}%")
ax.set_ylabel("Annualised volatility (%)")
add_titles(ax, "NBB stayed more volatile than MERC throughout")
save_chart(fig, "ch20_ex4_rolling_vol.png",
           "ch20-ex4-rolling-vol.png")
