# applied_large_txns.py - large GBP transactions for review
from pathlib import Path

import pandas as pd

from nb_db import get_engine

pd.options.display.float_format = "{:,.2f}".format

month_start = "2025-03-01"
month_end = "2025-04-01"
currency = "GBP"
threshold = 1000

query = """
    SELECT transaction_id, account_id, txn_date,
           amount, currency, category, channel
    FROM dbo.transactions
    WHERE txn_date >= ? AND txn_date < ?
      AND currency = ?
      AND ABS(amount) >= ?
      AND category NOT IN ('Salary', 'Rent')
    ORDER BY ABS(amount) DESC;
"""
engine = get_engine()
large = pd.read_sql(
    query, engine,
    params=(month_start, month_end, currency, threshold),
)

print(len(large), "large GBP transactions in March 2025")
print(large.groupby(["category", "channel"])
      .agg(count=("transaction_id", "count"),
           total=("amount", "sum")))
print(large.head(5))

Path("output").mkdir(exist_ok=True)
large.to_csv("output/large_txns_2025-03.csv", index=False)
print("Written output/large_txns_2025-03.csv")
