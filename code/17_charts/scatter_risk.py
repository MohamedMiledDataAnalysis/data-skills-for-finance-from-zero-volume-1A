import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator

from nbcharts import nb_style, add_titles, save_chart, PALETTE

nb_style()

loans = pd.read_csv("data/csv/loans.csv")
customers = pd.read_csv("data/csv/customers.csv")
data = loans.merge(customers[["customer_id", "risk_rating"]],
                   on="customer_id", how="left")
personal = data[data["product"] == "Personal"]
print("Personal loans:", len(personal))

rng = np.random.default_rng(2026)
jitter = rng.uniform(-0.15, 0.15, size=len(personal))

slope, intercept = np.polyfit(personal["risk_rating"],
                              personal["interest_rate"], 1)
print(f"Trend: rate = {intercept:.2f} + {slope:.2f} x rating")
means = personal.groupby("risk_rating")["interest_rate"].mean()
print(means.round(2))

fig, ax = plt.subplots(figsize=(6, 3.6))
ax.scatter(personal["risk_rating"] + jitter,
           personal["interest_rate"], s=14, alpha=0.5,
           color=PALETTE["teal"], linewidths=0)
xs = np.array([1, 5])
ax.plot(xs, intercept + slope * xs, color=PALETTE["navy"],
        linewidth=1.5, label="Linear trend")
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xlabel("Customer risk rating (1 = lowest risk)")
ax.set_ylabel("Interest rate (% a year)")
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_formatter("{x:.0f}%")
ax.legend(loc="upper left")
add_titles(ax, "Riskier customers pay more on personal loans")
save_chart(fig, "ch17_scatter_risk.png", "ch17-scatter-risk.png")
