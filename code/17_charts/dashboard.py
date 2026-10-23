import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter, MonthLocator
from matplotlib.ticker import MultipleLocator

from nbcharts import (nb_style, save_chart, gbp_m, pct,
                      PALETTE, SOURCE)

nb_style()

loans = pd.read_csv("data/csv/loans.csv")
fx = pd.read_csv("data/csv/fx_rates.csv", parse_dates=["rate_date"])
prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])

principal = (loans.groupby("product")["principal"].sum()
             / 1_000_000).sort_values()
loans["not_performing"] = loans["status"] != "Performing"
arrears = (loans.groupby("product")["not_performing"].mean()
           * 100).sort_values()
eur = fx[fx["currency"] == "EUR"]
nbb = prices[prices["ticker"] == "NBB"]

fig, axes = plt.subplots(2, 2, figsize=(6, 4.8))
ax1, ax2, ax3, ax4 = axes.flatten()

ax1.barh(principal.index, principal.values,
         color=PALETTE["navy"], height=0.55)
ax1.xaxis.set_major_locator(MultipleLocator(50))
ax1.xaxis.set_major_formatter(gbp_m)
ax1.set_title("Principal by product", fontsize=9)
ax1.grid(axis="y", visible=False)

ax2.barh(arrears.index, arrears.values,
         color=PALETTE["red"], height=0.55)
ax2.xaxis.set_major_formatter(pct)
ax2.set_title("Loans not performing", fontsize=9)
ax2.grid(axis="y", visible=False)

ax3.plot(eur["rate_date"], eur["rate_per_gbp"],
         color=PALETTE["teal"])
ax3.set_title("EUR per £1", fontsize=9)
ax3.yaxis.set_major_locator(MultipleLocator(0.04))
ax3.yaxis.set_major_formatter("€{x:.2f}")

ax4.plot(nbb["price_date"], nbb["close"], color=PALETTE["navy"])
ax4.set_title("NBB share price", fontsize=9)
ax4.yaxis.set_major_formatter("£{x:.0f}")

for ax in (ax3, ax4):
    ax.xaxis.set_major_locator(MonthLocator(bymonth=[1, 5, 9]))
    ax.xaxis.set_major_formatter(DateFormatter("%b"))

fig.suptitle("Northbridge Bank at a glance, 2025", x=0.02,
             ha="left", fontsize=11, fontweight="bold",
             color=PALETTE["navy"])
fig.text(0.02, 0.935, SOURCE, fontsize=8, va="top",
         color=PALETTE["slate"])
fig.tight_layout(rect=(0, 0, 1, 0.91), h_pad=1.5, w_pad=1.5)
save_chart(fig, "ch17_dashboard.png", "ch17-dashboard.png")
