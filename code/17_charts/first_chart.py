import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
balance = [12500, 13100, 12800, 14250, 14900, 15400]

fig, ax = plt.subplots()
ax.plot(months, balance)
ax.set_title("Savings balance, first half of 2025")
ax.set_xlabel("Month")
ax.set_ylabel("Balance (£)")
fig.savefig("output/ch17_first_chart.png", dpi=200,
            bbox_inches="tight")
print(type(fig).__name__, type(ax).__name__)
