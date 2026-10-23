# ex2_customer_accounts.py - Exercise 2, one customer's accounts
import pandas as pd

from nb_db import get_engine

engine = get_engine()
customer_id = "C0005"
accounts = pd.read_sql(
    """
    SELECT account_id, account_type, currency, balance
    FROM dbo.accounts
    WHERE customer_id = ?
    ORDER BY account_id;
    """,
    engine,
    params=(customer_id,),
)
print(accounts)
print(f"Total: {accounts['balance'].sum():,.2f}")
