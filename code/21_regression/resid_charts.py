# resid_charts.py - histogram and scatter of the residuals
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

from regdata import load_loans, split

sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import nb_style, add_titles, save_chart, PALETTE

train, test = split(load_loans())
model = smf.ols("interest_rate ~ risk_rating + C(product)",
                data=train).fit()
train["fitted"] = model.fittedvalues
train["residual"] = train["interest_rate"] - train["fitted"]

nb_style()
fig, ax = plt.subplots(figsize=(6, 3.4))
ax.hist(train["residual"], bins=30, color=PALETTE["navy"],
        edgecolor="white", linewidth=0.6)
ax.axvline(0, color=PALETTE["red"], linewidth=1.5)
ax.set_xlabel("Residual = actual rate - fitted rate "
              "(percentage points)")
ax.set_ylabel("Number of loans")
add_titles(ax, "Residuals are centred on zero and symmetric")
save_chart(fig, "ch21_resid_hist.png", "ch21-resid-hist.png")

fig, ax = plt.subplots(figsize=(6, 3.4))
ax.scatter(train["fitted"], train["residual"], s=10,
           alpha=0.5, color=PALETTE["teal"], linewidths=0)
ax.axhline(0, color=PALETTE["red"], linewidth=1.5)
ax.set_xlabel("Fitted rate (% a year)")
ax.set_ylabel("Residual (percentage points)")
ax.xaxis.set_major_formatter("{x:.0f}%")
add_titles(ax, "No pattern in the residuals against fitted rates")
save_chart(fig, "ch21_resid_fitted.png", "ch21-resid-fitted.png")
