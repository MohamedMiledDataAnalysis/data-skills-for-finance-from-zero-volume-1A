# ex1_usd_june.py - Exercise 1, dollar rates for June
import requests

response = requests.get(
    "http://127.0.0.1:8000/fx-rates",
    params={"currency": "USD", "month": "2025-06"},
    timeout=10,
)
response.raise_for_status()
data = response.json()
values = [r["rate_per_gbp"] for r in data["rates"]]
print("Business days:", data["count"])
print("Average USD per £1:", round(sum(values) / len(values), 4))
print("First:", data["rates"][0]["date"],
      "Last:", data["rates"][-1]["date"])
