# fx_rates.py - query parameters with params
import requests

BASE_URL = "http://127.0.0.1:8000"

response = requests.get(
    f"{BASE_URL}/fx-rates",
    params={"currency": "EUR", "month": "2025-03"},
    timeout=10,
)
print(response.url)
response.raise_for_status()

data = response.json()
print(type(data).__name__, list(data))
print(data["base"], data["count"])
print(data["rates"][0])
