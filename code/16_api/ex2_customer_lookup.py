# ex2_customer_lookup.py - Exercise 2, customer lookup
import os

import requests

BASE_URL = "http://127.0.0.1:8000"
headers = {"X-API-Key": os.environ.get("NB_API_KEY",
                                       "northbridge-demo")}

for customer_id in ["C0010", "C0999"]:
    response = requests.get(f"{BASE_URL}/customers/{customer_id}",
                            headers=headers, timeout=10)
    if response.status_code == 404:
        print(customer_id, "not found:",
              response.json()["error"])
        continue
    response.raise_for_status()
    customer = response.json()
    currencies = {a["currency"] for a in customer["accounts"]}
    assert len(currencies) == 1, f"mixed currencies: {currencies}"
    total = sum(a["balance"] for a in customer["accounts"])
    print(customer_id, customer["segment"],
          len(customer["accounts"]), "accounts,",
          f"total {total:,.2f}",
          customer["accounts"][0]["currency"])
