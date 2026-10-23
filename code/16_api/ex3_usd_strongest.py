# ex3_usd_strongest.py - Exercise 3, the strongest month
from pathlib import Path

import pandas as pd
import requests

response = requests.get("http://127.0.0.1:8000/fx-rates",
                        params={"currency": "USD"}, timeout=10)
response.raise_for_status()
usd = pd.DataFrame(response.json()["rates"])
usd["month"] = usd["date"].str[:7]

monthly = (usd.groupby("month")["rate_per_gbp"].mean()
           .round(4).rename("avg_usd_per_gbp"))
best = monthly.idxmax()
worst = monthly.idxmin()
print(monthly.head(3))
print("Strongest pound:", best, monthly[best])
print("Weakest pound:  ", worst, monthly[worst])

Path("output").mkdir(exist_ok=True)
monthly.to_csv("output/usd_monthly_avg.csv")
print(pd.read_csv("output/usd_monthly_avg.csv").shape)
