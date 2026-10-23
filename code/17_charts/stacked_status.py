import matplotlib.pyplot as plt
import pandas as pd

from nbcharts import nb_style, add_titles, save_chart, pct, PALETTE

nb_style()

loans = pd.read_csv("data/csv/loans.csv")
statuses = ["Performing", "30+ DPD", "90+ DPD", "Default"]
counts = pd.crosstab(loans["product"], loans["status"])
counts = counts[statuses]
shares = counts.div(counts.sum(axis=1), axis=0) * 100
shares = shares.sort_values("Performing")
print(counts)
print(shares.round(1))

colours = [PALETTE["sand"], PALETTE["gold"],
           PALETTE["slate"], PALETTE["red"]]
fig, ax = plt.subplots(figsize=(6, 3.2))
left = pd.Series(0.0, index=shares.index)
for status, colour in zip(statuses, colours):
    ax.barh(shares.index, shares[status], left=left,
            color=colour, height=0.55, label=status,
            edgecolor="white", linewidth=1)
    left = left + shares[status]

for i, product in enumerate(shares.index):
    arrears = 100 - shares.loc[product, "Performing"]
    ax.text(101, i, f"{arrears:.1f}% not performing",
            va="center", fontsize=8, color="#333333")

ax.set_xlim(0, 135)
ax.set_xticks([0, 25, 50, 75, 100])
ax.xaxis.set_major_formatter(pct)
ax.set_xlabel("Share of loans in each product (%)")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
ax.legend(ncols=4, loc="upper left", bbox_to_anchor=(0, -0.2))
add_titles(ax, "Loan status mix by product")
save_chart(fig, "ch17_stacked_status.png",
           "ch17-stacked-status.png")
