# read_sql_pandas.py - a query result into pandas
import pandas as pd

from nb_db import get_engine

pd.options.display.float_format = "{:,.2f}".format

engine = get_engine()
query = """
    SELECT product,
           COUNT(*)       AS loans,
           SUM(principal) AS principal
    FROM dbo.loans
    GROUP BY product
    ORDER BY product;
"""
by_product = pd.read_sql(query, engine)
print(by_product)
print(by_product.dtypes)
