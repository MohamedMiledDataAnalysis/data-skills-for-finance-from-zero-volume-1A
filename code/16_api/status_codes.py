# status_codes.py - status codes 200, 401 and 404
import requests

BASE_URL = "http://127.0.0.1:8000"
key = {"X-API-Key": "northbridge-demo"}

tests = [("/health", {}), ("/loans", {}),
         ("/customers/C9999", key)]
for path, headers in tests:
    response = requests.get(BASE_URL + path, headers=headers,
                            timeout=10)
    print(path, response.status_code, response.reason)
    print("   ", response.json())

response = requests.get(BASE_URL + "/loans", timeout=10)
try:
    response.raise_for_status()
except requests.HTTPError as error:
    print("HTTPError:", error)
