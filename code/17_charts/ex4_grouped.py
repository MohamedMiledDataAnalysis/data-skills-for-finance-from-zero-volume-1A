import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from nbcharts import (nb_style, add_titles, save_chart,
                      gbp_m, PALETTE)

nb_style()

loans = pd.read_csv("data/csv/loans.csv")
customers = pd.read_csv("data/csv/customers.csv")
data = loans.merge(customers[["customer_id", "segment"]],
                   on="customer_id", how="left")
table = data.pivot_table(index="product", columns="segment",
                         values="principal", aggfunc="sum",
                         fill_value=0) / 1_000_000
table = table[["Retail", "Private", "SME"]]
print(table.round(2))

x = np.arange(len(table.index))
width = 0.26
colours = [PALETTE["navy"], PALETTE["teal"], PALETTE["gold"]]
fig, ax = plt.subplots(figsize=(6, 3.4))
for i, (segment, colour) in enumerate(zip(table.columns, colours)):
    ax.bar(x + (i - 1) * width, table[segment], width=width,
           color=colour, label=segment,
           edgecolor="white", linewidth=1)
ax.set_xticks(x, table.index)
ax.yaxis.set_major_formatter(gbp_m)
ax.set_ylabel("Total principal (£ millions)")
ax.grid(axis="x", visible=False)
ax.legend(title="Customer segment", loc="upper left")
add_titles(ax, "Loan principal by product and segment")
save_chart(fig, "ch17_ex4_grouped.png", "ch17-ex4.png")
