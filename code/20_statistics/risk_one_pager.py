# risk_one_pager.py - Applied example: market risk summary
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import nb_style, add_titles, save_chart, PALETTE

RF = 0.04             # ASSUMPTION: risk-free rate, 4% a year
POSITION = 1_000_000  # position size for VaR: £1,000,000
DAYS_YEAR = 261       # weekday rows per year in this file

prices = pd.read_csv("data/csv/market_prices.csv",
                     parse_dates=["price_date"])
prices = prices.sort_values(["ticker", "price_date"])
g = prices.groupby("ticker")["close"]
prices["ret"] = g.pct_change()
prices["drawdown"] = prices["close"] / g.cummax() - 1


def risk_row(t):
    """All the risk figures for one ticker's rows."""
    r = t["ret"].dropna()
    total = t["close"].iloc[-1] / t["close"].iloc[0] - 1
    ann_ret = (1 + total) ** (DAYS_YEAR / len(r)) - 1
    ann_vol = r.std() * np.sqrt(DAYS_YEAR)
    best, worst = r.idxmax(), r.idxmin()
    return pd.Series({
        "ann_return_pct": 100 * ann_ret,
        "ann_vol_pct": 100 * ann_vol,
        "sharpe": (ann_ret - RF) / ann_vol,
        "max_drawdown_pct": 100 * t["drawdown"].min(),
        "var95_1d_gbp": -r.quantile(0.05) * POSITION,
        "best_day_pct": 100 * r.max(),
        "best_date": t.loc[best, "price_date"].date(),
        "worst_day_pct": 100 * r.min(),
        "worst_date": t.loc[worst, "price_date"].date(),
    })


cols = ["price_date", "close", "ret", "drawdown"]
risk = (prices.groupby("ticker")[cols].apply(risk_row)
        .sort_values("sharpe", ascending=False))
report = risk.round({"ann_return_pct": 1, "ann_vol_pct": 1,
                     "sharpe": 2, "max_drawdown_pct": 1,
                     "var95_1d_gbp": 0, "best_day_pct": 2,
                     "worst_day_pct": 2})
report["var95_1d_gbp"] = report["var95_1d_gbp"].astype(int)
report.to_csv("output/risk_one_pager.csv")
print(report.iloc[:, :4].to_string())   # three prints keep
print(report.iloc[:, 4:7].to_string())  # each table narrow
print(report.iloc[:, 7:].to_string())

nb_style()
fig, ax = plt.subplots()
size = -15 * report["max_drawdown_pct"]  # area ~ drawdown
ax.scatter(report["ann_vol_pct"], report["ann_return_pct"],
           s=size, color=PALETTE["navy"], alpha=0.85,
           edgecolor="white", linewidth=1)
for ticker, row in report.iterrows():
    ax.annotate(f"{ticker}  Sharpe {row['sharpe']:.2f}\n"
                f"drawdown {row['max_drawdown_pct']:.1f}%",
                (row["ann_vol_pct"], row["ann_return_pct"]),
                xytext=(14, 0), textcoords="offset points",
                va="center", fontsize=8, color="#333333")
ax.set_xlim(10, 50)
ax.set_ylim(15, 25)
ax.xaxis.set_major_formatter("{x:.0f}%")
ax.yaxis.set_major_formatter("{x:.0f}%")
ax.set_xlabel("Annualised volatility (%)")
ax.set_ylabel("Annualised return (%)")
ax.text(0.98, 0.04, "Point area = maximum drawdown\n"
        "Sharpe assumes a 4% risk-free rate", ha="right",
        transform=ax.transAxes, fontsize=8, color=PALETTE["slate"])
add_titles(ax, "Return against risk, four shares, 2025")
save_chart(fig, "ch20_risk_return.png", "ch20-risk-return.png")
