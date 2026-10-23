# api_key.py - send the API key in a header
import requests

BASE_URL = "http://127.0.0.1:8000"
headers = {"X-API-Key": "northbridge-demo"}

response = requests.get(f"{BASE_URL}/customers/C0005",
                        headers=headers, timeout=10)
response.raise_for_status()
customer = response.json()
print(customer["first_name"], customer["last_name"],
      customer["address"]["city"])
for account in customer["accounts"]:
    print(account["account_id"], account["currency"],
          account["balance"])
