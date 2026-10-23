# frankfurter.py - ECB exchange rates from Frankfurter
import pandas as pd

from retry import get_with_retry

URL = "https://api.frankfurter.dev/v2/rates"
params = {"base": "EUR", "quotes": "GBP", "providers": "ECB",
          "from": "2025-01-02", "to": "2025-01-08"}

response = get_with_retry(URL, params=params)
print(response.url)

rates = pd.DataFrame(response.json())
rates["date"] = pd.to_datetime(rates["date"])
rates["eur_per_gbp"] = (1 / rates["rate"]).round(4)
print(rates)
