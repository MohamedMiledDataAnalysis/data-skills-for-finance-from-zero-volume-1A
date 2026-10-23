# read_in_chunks.py - read a large table in chunks
import pandas as pd

from nb_db import get_engine

engine = get_engine()
query = """
    SELECT transaction_id, category, amount
    FROM dbo.transactions;
"""
totals = {}
rows = 0
for chunk in pd.read_sql(query, engine, chunksize=5000):
    rows += len(chunk)
    print("chunk of", len(chunk), "rows")
    sums = chunk.groupby("category")["amount"].sum()
    for category, amount in sums.items():
        totals[category] = totals.get(category, 0) + amount

print("Rows read:", rows)
for category, amount in sorted(totals.items()):
    print(f"{category:<12}£{amount:>14,.2f}")
