import matplotlib.pyplot as plt
import pandas as pd

from nbcharts import (nb_style, save_chart, thousands,
                      PALETTE, SOURCE)

nb_style()

txns = pd.read_csv("data/csv/transactions.csv",
                   parse_dates=["txn_date"])
txns["month"] = txns["txn_date"].dt.month
counts = pd.crosstab(txns["month"], txns["channel"])
print(counts.head(3))
print("Total:", counts.to_numpy().sum())

channels = ["Online", "Card", "Mobile", "Branch"]
fig, axes = plt.subplots(2, 2, figsize=(6, 4.4),
                         sharex=True, sharey=True)
for ax, channel in zip(axes.flatten(), channels):
    for other in channels:
        ax.plot(counts.index, counts[other],
                color="#C8CDD6", linewidth=0.8)
    ax.plot(counts.index, counts[channel],
            color=PALETTE["navy"], linewidth=1.8)
    ax.set_title(channel, fontsize=9)
    ax.set_xticks([1, 4, 7, 10], ["Jan", "Apr", "Jul", "Oct"])
    ax.yaxis.set_major_formatter(thousands)
    ax.set_ylim(0)

fig.suptitle("Transactions per month by channel, 2025",
             x=0.02, ha="left", fontsize=11, fontweight="bold",
             color=PALETTE["navy"])
fig.text(0.02, 0.935, SOURCE, fontsize=8, va="top",
         color=PALETTE["slate"])
fig.supylabel("Number of transactions", fontsize=9)
fig.tight_layout(rect=(0, 0, 1, 0.92))
save_chart(fig, "ch17_ex5_channels.png", "ch17-ex5.png")
