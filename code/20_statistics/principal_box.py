# principal_box.py - box plots of principal by product
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import nb_style, add_titles, save_chart, PALETTE

loans = pd.read_csv("data/csv/loans.csv")
order = (loans.groupby("product")["principal"].median()
         .sort_values().index.tolist())
groups = [loans.loc[loans["product"] == name, "principal"]
          for name in order]

nb_style()
fig, ax = plt.subplots()
ax.boxplot(groups, tick_labels=order, widths=0.55,
           patch_artist=True,
           boxprops={"facecolor": PALETTE["sand"],
                     "edgecolor": PALETTE["navy"]},
           medianprops={"color": PALETTE["navy"], "linewidth": 2},
           whiskerprops={"color": PALETTE["navy"]},
           capprops={"color": PALETTE["navy"]},
           flierprops={"marker": "o", "markersize": 3.5,
                       "markerfacecolor": PALETTE["red"],
                       "markeredgecolor": "white"})
ax.set_yscale("log")
ax.set_yticks([2e3, 5e3, 1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6],
              ["£2k", "£5k", "£10k", "£20k", "£50k", "£100k",
               "£200k", "£500k", "£1m"])
ax.minorticks_off()
ax.set_ylabel("Principal (£, log scale)")
ax.grid(axis="x", visible=False)
add_titles(ax, "Mortgages and SME loans dwarf consumer loans")
save_chart(fig, "ch20_principal_box.png", "ch20-principal-box.png")
