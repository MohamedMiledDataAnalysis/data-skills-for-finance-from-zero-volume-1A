# ex5_fx_monthly.py - Exercise 5, monthly FX averages
import pandas as pd

from nb_db import get_engine

engine = get_engine()
fx = pd.read_sql(
    "SELECT rate_date, currency, rate_per_gbp FROM dbo.fx_rates;",
    engine,
    parse_dates=["rate_date"],
)
fx["month"] = fx["rate_date"].dt.strftime("%Y-%m")
monthly = (fx.groupby(["month", "currency"])["rate_per_gbp"]
           .mean().round(4).reset_index(name="avg_rate"))

monthly.to_sql("fx_monthly_avg", engine, schema="dbo",
               if_exists="replace", index=False)

back = pd.read_sql(
    """
    SELECT month, currency, avg_rate
    FROM dbo.fx_monthly_avg
    WHERE currency = ?
    ORDER BY month;
    """,
    engine, params=("EUR",),
)
print(len(monthly), "rows written")
print(back.head(3))
print(back.tail(1))
