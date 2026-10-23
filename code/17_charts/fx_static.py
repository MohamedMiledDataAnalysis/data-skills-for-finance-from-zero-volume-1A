import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter, MonthLocator
from matplotlib.ticker import MultipleLocator

from nbcharts import nb_style, add_titles, save_chart, PALETTE

nb_style()

fx = pd.read_csv("data/csv/fx_rates.csv", parse_dates=["rate_date"])
wide = fx.pivot(index="rate_date", columns="currency",
                values="rate_per_gbp")

fig, ax = plt.subplots(figsize=(6, 3.4))
ax.plot(wide.index, wide["EUR"], label="EUR per £1",
        color=PALETTE["navy"])
ax.plot(wide.index, wide["USD"], label="USD per £1",
        color=PALETTE["teal"])
ax.yaxis.set_major_locator(MultipleLocator(0.05))
ax.yaxis.set_major_formatter("{x:.2f}")
ax.set_ylabel("Units of currency per £1")
ax.xaxis.set_major_locator(MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(DateFormatter("%b %Y"))
ax.legend(loc="lower left", ncols=2)
add_titles(ax, "EUR and USD per £1, 2025")
save_chart(fig, "ch17_fx_static.png", "ch17-fx-rates.png")
