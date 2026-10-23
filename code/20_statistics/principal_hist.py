# principal_hist.py - histogram of loan principal, log scale
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Reuse the chart style from Chapter 17.
sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import nb_style, add_titles, save_chart, PALETTE

loans = pd.read_csv("data/csv/loans.csv")
p = loans["principal"]
med, avg = p.median(), p.mean()

ticks = [2e3, 5e3, 1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6]
labels = ["£2k", "£5k", "£10k", "£20k", "£50k",
          "£100k", "£200k", "£500k", "£1m"]
bins = np.geomspace(p.min(), p.max(), 41)  # 40 log-width bins

nb_style()
fig, ax = plt.subplots()
counts, edges, bars = ax.hist(p, bins=bins,
                              color=PALETTE["teal"],
                              edgecolor="white", linewidth=0.4)
ax.set_ylim(0, counts.max() * 1.15)  # room for labels
ax.set_xscale("log")
ax.set_xticks(ticks, labels)
ax.minorticks_off()
for value, colour, text, side in [
        (med, "navy", f"Median £{med / 1000:.0f}k", "right"),
        (avg, "red", f"Mean £{avg / 1000:.0f}k", "left")]:
    ax.axvline(value, color=PALETTE[colour], linewidth=1.2)
    gap = 0.96 if side == "right" else 1.04
    ax.text(value * gap, 0.97, text, ha=side, va="top",
            transform=ax.get_xaxis_transform(), fontsize=8,
            color="#333333")
ax.set_xlabel("Principal (£, log scale)")
ax.set_ylabel("Number of loans")
ax.grid(axis="x", visible=False)
add_titles(ax, "Loan sizes span three orders of magnitude")
save_chart(fig, "ch20_principal_hist.png",
           "ch20-principal-hist.png")
