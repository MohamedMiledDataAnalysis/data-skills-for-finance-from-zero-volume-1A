# api_key_env.py - the API key from an environment variable
import os

import requests

BASE_URL = "http://127.0.0.1:8000"

api_key = os.environ.get("NB_API_KEY")
if api_key is None:
    raise SystemExit("Set the NB_API_KEY environment variable "
                     "before running this script.")

response = requests.get(
    f"{BASE_URL}/loans",
    params={"product": "Auto", "page": 1},
    headers={"X-API-Key": api_key},
    timeout=10,
)
if response.status_code == 401:
    raise SystemExit("401 Unauthorized: check the value of "
                     "NB_API_KEY.")
response.raise_for_status()
body = response.json()
print("page", body["page"], "of", body["pages"],
      "| total", body["total"], "| this page",
      len(body["loans"]))
