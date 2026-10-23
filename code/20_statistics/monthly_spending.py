# monthly_spending.py - monthly spending, trend and changes
import sys
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import nb_style, add_titles, save_chart, PALETTE

fx = pd.read_csv("data/csv/fx_rates.csv", parse_dates=["rate_date"])
fx_month = (fx.set_index("rate_date").groupby("currency")
            ["rate_per_gbp"].resample("ME").mean().reset_index())

txn = pd.read_csv("data/csv/transactions.csv",
                  parse_dates=["txn_date"])
spend = txn[(txn["amount"] < 0)
            & (txn["category"] != "Transfer")].copy()
spend["month"] = spend["txn_date"] + pd.offsets.MonthEnd(0)
spend = spend.merge(fx_month, how="left",
                    left_on=["month", "currency"],
                    right_on=["rate_date", "currency"])
spend.loc[spend["currency"] == "GBP", "rate_per_gbp"] = 1.0
spend["spend_gbp"] = -spend["amount"] / spend["rate_per_gbp"]

monthly = (spend.groupby("month")["spend_gbp"].sum()
           .to_frame("total"))
monthly["ma3"] = monthly["total"].rolling(3).mean()
monthly["mom_pct"] = 100 * monthly["total"].pct_change()
monthly["ytd"] = monthly["total"].cumsum()
print(monthly.to_string(float_format="{:,.0f}".format,
                        formatters={"mom_pct": "{:.1f}".format}))

x = monthly.index.to_period("M").to_timestamp()  # 1st of month
nb_style()
fig, ax = plt.subplots()
ax.plot(x, monthly["total"] / 1000,
        color=PALETTE["slate"], linewidth=1, label="Monthly total")
ax.plot(x, monthly["ma3"] / 1000,
        color=PALETTE["navy"], linewidth=2.2,
        label="3-month moving average")
ax.set_ylim(0, None)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.yaxis.set_major_locator(MultipleLocator(50))
ax.yaxis.set_major_formatter("£{x:,.0f}k")
ax.set_ylabel("Spending per month (£ thousands)")
ax.legend(loc="lower right")
add_titles(ax, "Customer spending held steady through 2025")
save_chart(fig, "ch20_spending_trend.png",
           "ch20-spending-trend.png")
