import matplotlib.pyplot as plt
import pandas as pd

from nbcharts import nb_style, add_titles, save_chart, PALETTE

nb_style()

loans = pd.read_csv("data/csv/loans.csv")
customers = pd.read_csv("data/csv/customers.csv")
data = loans.merge(customers[["customer_id", "risk_rating"]],
                   on="customer_id", how="left")
personal = data[data["product"] == "Personal"]

ratings = [1, 2, 3, 4, 5]
groups = [personal.loc[personal["risk_rating"] == r,
                       "interest_rate"] for r in ratings]
summary = personal.groupby("risk_rating")["interest_rate"]
print(summary.describe()[["count", "25%", "50%", "75%"]])

one = groups[0]
q1, q3 = one.quantile(0.25), one.quantile(0.75)
iqr = q3 - q1
print(f"Rating 1: IQR {iqr:.3f}, upper limit {q3 + 1.5 * iqr:.3f}")
print("Outliers:", one[one > q3 + 1.5 * iqr].tolist())

fig, ax = plt.subplots(figsize=(6, 3.6))
ax.boxplot(groups, tick_labels=ratings, widths=0.5,
           patch_artist=True, showfliers=True,
           boxprops={"facecolor": PALETTE["sand"],
                     "edgecolor": PALETTE["navy"]},
           medianprops={"color": PALETTE["navy"],
                        "linewidth": 2},
           whiskerprops={"color": PALETTE["navy"]},
           capprops={"color": PALETTE["navy"]},
           flierprops={"marker": "o", "markersize": 4,
                       "markerfacecolor": PALETTE["red"],
                       "markeredgecolor": "white"})
ax.set_xlabel("Customer risk rating (1 = lowest risk)")
ax.set_ylabel("Interest rate (% a year)")
ax.yaxis.set_major_formatter("{x:.1f}%")
ax.grid(axis="x", visible=False)
add_titles(ax, "Personal loan rates by risk rating")
save_chart(fig, "ch17_boxplot_rates.png", "ch17-boxplot.png")
