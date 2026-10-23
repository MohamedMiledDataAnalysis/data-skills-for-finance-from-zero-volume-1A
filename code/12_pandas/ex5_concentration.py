# ex5_concentration.py - Exercise 5: top 10 borrowers
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")

by_customer = loans.groupby("customer_id").agg(
    loans=("loan_id", "count"),
    exposure=("principal", "sum"),
)
top10 = by_customer.nlargest(10, "exposure")
total = loans["principal"].sum()
top10["share_pct"] = (top10["exposure"] / total * 100).round(2)

print(top10.round(2))
print(f"Borrowers: {len(by_customer)}")
top_share = top10["exposure"].sum() / total * 100
print(f"Top 10 share of book: {top_share:.2f}%")
top10.to_csv("output/top10_borrowers.csv")
