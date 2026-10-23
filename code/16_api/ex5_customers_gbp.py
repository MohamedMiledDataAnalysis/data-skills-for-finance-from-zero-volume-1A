# ex5_customers_gbp.py - Exercise 5, twenty customers in pounds
import pandas as pd

from retry import get_with_retry

BASE_URL = "http://127.0.0.1:8000"
headers = {"X-API-Key": "northbridge-demo"}

# Month-end rates for December 2025
last = {"GBP": 1.0}
for ccy in ["EUR", "USD"]:
    body = get_with_retry(f"{BASE_URL}/fx-rates",
                          params={"currency": ccy,
                                  "month": "2025-12"}).json()
    last[ccy] = body["rates"][-1]["rate_per_gbp"]
print("31 Dec 2025 rates:", last)

# Customers C0001 to C0020, one request each
customers = []
for i in range(1, 21):
    url = f"{BASE_URL}/customers/C{i:04d}"
    customers.append(get_with_retry(url,
                                    headers=headers).json())

accounts = pd.json_normalize(customers, record_path="accounts",
                             meta=["customer_id", "segment"])
accounts["balance_gbp"] = (accounts["balance"]
                           / accounts["currency"].map(last))
print(len(customers), "customers,", len(accounts), "accounts")
print(accounts.groupby("currency")
      .agg(accounts=("account_id", "count"),
           balance=("balance", "sum"),
           balance_gbp=("balance_gbp", "sum")).round(2))
print(f"Total in GBP: £{accounts['balance_gbp'].sum():,.2f}")
