# health.py - your first API request
import requests

response = requests.get("http://127.0.0.1:8000/health",
                        timeout=10)
print(response.status_code)
print(response.headers["Content-Type"])
print(response.text)
print(response.json())
