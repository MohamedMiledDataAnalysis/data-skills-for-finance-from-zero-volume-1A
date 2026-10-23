# ex3_high_ltv.py - Exercise 3: high-LTV mortgages in arrears
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")

high = loans[(loans["product"] == "Mortgage") & (loans["ltv"] > 80)]
print(f"High-LTV mortgages: {len(high)}, "
      f"£{high['principal'].sum():,.2f}")

bad = high[high["status"].isin(["90+ DPD", "Default"])]
cols = ["loan_id", "customer_id", "principal", "ltv", "status"]
print(bad[cols].sort_values("ltv", ascending=False))
bad[cols].to_csv("output/high_ltv_watchlist.csv", index=False)
