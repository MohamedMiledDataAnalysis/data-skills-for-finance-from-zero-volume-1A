import matplotlib.pyplot as plt
import pandas as pd

from nbcharts import (nb_style, add_titles, save_chart,
                      gbp_m, PALETTE)

nb_style()

loans = pd.read_csv("data/csv/loans.csv")
by_product = (loans.groupby("product")["principal"].sum()
              / 1_000_000).sort_values()
print(by_product.round(2))

fig, ax = plt.subplots(figsize=(6, 3))
bars = ax.barh(by_product.index, by_product.values,
               color=PALETTE["navy"], height=0.55)
ax.bar_label(bars, labels=[f"£{v:,.1f}m" for v in by_product],
             padding=4, fontsize=8, color="#333333")
ax.xaxis.set_major_formatter(gbp_m)
ax.set_xlim(0, by_product.max() * 1.15)
ax.set_xlabel("Total principal (£ millions)")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)
add_titles(ax, "Mortgages hold most of the loan book")
save_chart(fig, "ch17_bar_principal.png", "ch17-bar-principal.png")
