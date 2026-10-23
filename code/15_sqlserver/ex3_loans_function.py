# ex3_loans_function.py - Exercise 3, a reusable query
import pandas as pd

from nb_db import get_engine

ENGINE = get_engine()


def large_loans(product, min_principal):
    """Return loans of one product at or above a principal."""
    query = """
        SELECT loan_id, customer_id, principal, status
        FROM dbo.loans
        WHERE product = ? AND principal >= ?
        ORDER BY principal DESC;
    """
    return pd.read_sql(query, ENGINE,
                       params=(product, min_principal))


mortgages = large_loans("Mortgage", 600000)
print(mortgages)
sme = large_loans("SME", 600000)
print(len(sme), "SME loans of £600,000 or more")
