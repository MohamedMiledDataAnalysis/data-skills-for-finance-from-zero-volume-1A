# fx_monthly_avg.py - monthly average EUR rate
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:8000"

response = requests.get(f"{BASE_URL}/fx-rates",
                        params={"currency": "EUR"}, timeout=10)
response.raise_for_status()
rates = pd.DataFrame(response.json()["rates"])
rates["date"] = pd.to_datetime(rates["date"])
print(rates.shape)
print(rates.head(3))

rates["month"] = rates["date"].dt.strftime("%Y-%m")
monthly = (rates.groupby("month")["rate_per_gbp"]
           .agg(["mean", "min", "max"]).round(4))
print(monthly)

Path("output").mkdir(exist_ok=True)
monthly.to_csv("output/eur_monthly_avg.csv")
print("Written output/eur_monthly_avg.csv")
