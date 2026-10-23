# ex1_balances.py - Exercise 1: balances in GBP by segment
import pandas as pd

accounts = pd.read_csv("data/csv/accounts.csv")
customers = pd.read_csv("data/csv/customers.csv")
fx = pd.read_csv("data/csv/fx_rates.csv")
year_end = (fx[fx["rate_date"] == "2025-12-31"]
            [["currency", "rate_per_gbp"]])

bal = (accounts
       .merge(customers[["customer_id", "segment"]],
              on="customer_id", how="left")
       .merge(year_end, on="currency", how="left"))
bal.loc[bal["currency"] == "GBP", "rate_per_gbp"] = 1.0
bal["balance_gbp"] = bal["balance"] / bal["rate_per_gbp"]

stats = bal.groupby("segment")["balance_gbp"].agg(
    n="size", mean="mean", median="median", sd="std",
    p90=lambda s: s.quantile(0.90), max="max",
)
print(stats.sort_values("median", ascending=False).round(0)
      .astype(int))
