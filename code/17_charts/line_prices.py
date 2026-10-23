import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter, MonthLocator

from nbcharts import nb_style, add_titles, save_chart

nb_style()

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
wide = prices.pivot(index="price_date", columns="ticker",
                    values="close")
first_day = wide.index.min()
rebased = wide / wide.loc[first_day] * 100
print("First date:", first_day.date())
print(rebased.iloc[-1].round(1).sort_values(ascending=False))

fig, ax = plt.subplots(figsize=(6, 3.6))
for ticker in ["NBB", "ATLS", "GRNE", "MERC"]:
    ax.plot(rebased.index, rebased[ticker], label=ticker)

ax.axhline(100, color="#9AA3B2", linewidth=0.8)
ax.set_ylabel("Index (1 Jan 2025 = 100)")
ax.xaxis.set_major_locator(MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))
ax.legend(loc="upper left", bbox_to_anchor=(0, -0.1), ncols=4)
add_titles(ax, "Share prices rebased to 100, 2025")
save_chart(fig, "ch17_line_prices.png", "ch17-line-prices.png")
