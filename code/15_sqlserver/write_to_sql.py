# write_to_sql.py - write a DataFrame to SQL Server
import pandas as pd

from nb_db import get_engine

engine = get_engine()
loans = pd.read_sql(
    "SELECT product, status, principal FROM dbo.loans;",
    engine,
)
summary = (loans.groupby(["product", "status"])
           .agg(loans=("principal", "size"),
                principal=("principal", "sum"))
           .reset_index())
summary["principal"] = summary["principal"].round(2)

summary.to_sql("loan_status_summary", engine,
               schema="dbo", if_exists="replace", index=False)

check = pd.read_sql(
    "SELECT COUNT(*) AS n FROM dbo.loan_status_summary;",
    engine,
)
print("Rows written:", check.loc[0, "n"])
