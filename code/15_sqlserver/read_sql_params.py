# read_sql_params.py - read_sql with parameters
import pandas as pd

from nb_db import get_engine

engine = get_engine()
query = """
    SELECT txn_date, account_id, amount, channel
    FROM dbo.transactions
    WHERE category = ? AND currency = ? AND amount < ?
    ORDER BY amount;
"""
big_travel = pd.read_sql(query, engine,
                         params=("Travel", "GBP", -2000))
print(len(big_travel), "transactions")
print(big_travel.head())
