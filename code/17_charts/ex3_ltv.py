import matplotlib.pyplot as plt
import pandas as pd

from nbcharts import nb_style, add_titles, save_chart, pct, PALETTE

nb_style()

loans = pd.read_csv("data/csv/loans.csv")
ltv = loans.loc[loans["product"] == "Mortgage", "ltv"].dropna()
high = (ltv > 80).mean() * 100
print(f"Median LTV: {ltv.median():.1f}%")
print(f"Share above 80%: {high:.1f}%")

fig, ax = plt.subplots(figsize=(6, 3.4))
ax.hist(ltv, bins=range(45, 100, 5), color=PALETTE["teal"],
        edgecolor="white", linewidth=1)
ax.axvline(ltv.median(), color=PALETTE["navy"], linewidth=1.5)
ax.axvline(80, color=PALETTE["red"], linewidth=1.5)
top = ax.get_ylim()[1]
ax.text(ltv.median() - 1, top * 0.97,
        f"Median {ltv.median():.1f}%", ha="right", va="top",
        fontsize=8, color="#333333")
ax.text(81, top * 0.97, f"{high:.1f}% above 80%",
        ha="left", va="top", fontsize=8, color="#333333")
ax.set_ylim(0, top * 1.05)
ax.xaxis.set_major_formatter(pct)
ax.set_xlabel("Loan-to-value (%)")
ax.set_ylabel("Number of mortgages")
ax.grid(axis="x", visible=False)
add_titles(ax, "Mortgage loan-to-value distribution")
save_chart(fig, "ch17_ex3_ltv.png", "ch17-ex3.png")
