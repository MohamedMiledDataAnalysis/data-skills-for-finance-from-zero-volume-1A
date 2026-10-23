import matplotlib.pyplot as plt
import pandas as pd

from nbcharts import nb_style, add_titles, save_chart, PALETTE

nb_style()

customers = pd.read_csv("data/csv/customers.csv")
counts = customers["segment"].value_counts()
print(counts)

fig, ax = plt.subplots(figsize=(5, 3.2))
bars = ax.bar(counts.index, counts.values,
              color=PALETTE["navy"], width=0.5)
ax.bar_label(bars, padding=3, fontsize=8, color="#333333")
ax.set_ylabel("Number of customers")
ax.set_ylim(0, counts.max() * 1.12)
ax.grid(axis="x", visible=False)
add_titles(ax, "Customers by segment")
save_chart(fig, "ch17_ex1_segments.png", "ch17-ex1.png")
