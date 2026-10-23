# scatter_line.py - rate against risk rating, with the fitted line
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import statsmodels.formula.api as smf
from matplotlib.ticker import MultipleLocator

from regdata import load_loans, split

# Reuse the chart style from Chapter 17.
sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import nb_style, add_titles, save_chart, PALETTE

train, test = split(load_loans())
model = smf.ols("interest_rate ~ risk_rating", data=train).fit()
a, b = model.params

nb_style()
rng = np.random.default_rng(2026)
fig, ax = plt.subplots(figsize=(6, 3.8))
colours = ["navy", "teal", "gold", "slate"]
for name, colour in zip(["Mortgage", "Auto", "SME", "Personal"],
                        colours):
    part = train[train["product"] == name]
    jitter = rng.uniform(-0.18, 0.18, size=len(part))
    ax.scatter(part["risk_rating"] + jitter,
               part["interest_rate"], s=10, alpha=0.55,
               color=PALETTE[colour], linewidths=0, label=name)
xs = np.array([0.8, 5.2])
ax.plot(xs, a + b * xs, color=PALETTE["red"], linewidth=2,
        label=f"Fitted line: {a:.2f} + {b:.2f} x rating")
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xlabel("Customer risk rating (1 = lowest risk)")
ax.set_ylabel("Interest rate (% a year)")
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_formatter("{x:.0f}%")
ax.legend(loc="upper left", ncols=2, markerscale=1.6)
ax.set_ylim(2, 11.5)
add_titles(ax, "Interest rate rises with the risk rating")
save_chart(fig, "ch21_scatter_line.png", "ch21-scatter-line.png")
