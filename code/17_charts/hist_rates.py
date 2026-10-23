import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from nbcharts import nb_style, add_titles, save_chart, PALETTE

nb_style()

loans = pd.read_csv("data/csv/loans.csv")
rates = loans.loc[loans["product"] == "Mortgage", "interest_rate"]
median_rate = rates.median()
print("Mortgages:", len(rates))
print(f"Lowest {rates.min():.2f}%, highest {rates.max():.2f}%")
print(f"Median rate: {median_rate:.2f}%")

bins = np.arange(2.25, 6.01, 0.25)
fig, ax = plt.subplots(figsize=(6, 3.4))
ax.hist(rates, bins=bins, color=PALETTE["teal"],
        edgecolor="white", linewidth=1)
ax.axvline(median_rate, color=PALETTE["navy"], linewidth=1.5)
ax.annotate(f"Median {median_rate:.2f}%",
            xy=(median_rate, ax.get_ylim()[1] * 0.97),
            xytext=(6, 0), textcoords="offset points",
            ha="left", va="top", fontsize=8, color="#333333")
ax.xaxis.set_major_formatter("{x:.1f}%")
ax.set_xlabel("Interest rate (% a year)")
ax.set_ylabel("Number of mortgages")
ax.grid(axis="x", visible=False)
add_titles(ax, "Distribution of mortgage interest rates")
save_chart(fig, "ch17_hist_rates.png", "ch17-hist-rates.png")
