import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

from nbcharts import nb_style, add_titles, save_chart, PALETTE

nb_style()

txns = pd.read_csv("data/csv/transactions.csv",
                   parse_dates=["txn_date"])
accounts = pd.read_csv("data/csv/accounts.csv")
data = txns.merge(accounts[["account_id", "account_type"]],
                  on="account_id", how="left")
savings = data[(data["account_type"] == "Savings")
               & (data["currency"] == "GBP")].copy()
savings["month"] = savings["txn_date"].dt.strftime("%Y-%m")
net = savings.groupby("month")["amount"].sum()
labels = pd.to_datetime(net.index).strftime("%b")
print(net.round(2))

colours = [PALETTE["red"] if v < 0 else PALETTE["navy"]
           for v in net]
fig, ax = plt.subplots(figsize=(6, 3.4))
ax.bar(labels, net.values, color=colours, width=0.6)
ax.axhline(0, color="#333333", linewidth=0.8)


def signed_gbp(x, pos):
    sign = "-" if x < 0 else ""
    return f"{sign}£{abs(x):,.0f}"


ax.yaxis.set_major_formatter(FuncFormatter(signed_gbp))
for x, v in zip(labels, net.values):
    if v < 0:
        ax.annotate(signed_gbp(v, None), xy=(x, v),
                    xytext=(0, -4), textcoords="offset points",
                    ha="center", va="top", fontsize=8,
                    color="#333333")
ax.set_ylim(net.min() * 1.6, net.max() * 1.08)
ax.set_ylabel("Net cash flow (£)")
ax.grid(axis="x", visible=False)
add_titles(ax, "Net flow into GBP savings accounts, 2025")
save_chart(fig, "ch17_cashflow.png", "ch17-cashflow.png")
