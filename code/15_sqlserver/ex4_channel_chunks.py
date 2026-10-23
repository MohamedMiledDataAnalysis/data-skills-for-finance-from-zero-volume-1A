# ex4_channel_chunks.py - Exercise 4, channel counts in chunks
import pandas as pd

from nb_db import get_engine

engine = get_engine()
counts = pd.Series(dtype="int64")
total_rows = 0
for chunk in pd.read_sql(
        "SELECT channel FROM dbo.transactions;",
        engine, chunksize=4000):
    total_rows += len(chunk)
    counts = counts.add(chunk["channel"].value_counts(),
                        fill_value=0)

counts = counts.astype("int64").sort_values(ascending=False)
print(counts)
print("Rows read:", total_rows)
assert total_rows == counts.sum() == 20_000
