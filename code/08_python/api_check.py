# api_check.py - call the local Northbridge API with and
# without the API key
import requests

URL = "http://127.0.0.1:8000/loans?product=Mortgage&page=1"

no_key = requests.get(URL, timeout=10)
print("Without key:", no_key.status_code, no_key.json())

headers = {"X-API-Key": "northbridge-demo"}
with_key = requests.get(URL, headers=headers, timeout=10)
body = with_key.json()
print("With key:", with_key.status_code)
print("Mortgages:", body["total"], "in", body["pages"], "pages")
