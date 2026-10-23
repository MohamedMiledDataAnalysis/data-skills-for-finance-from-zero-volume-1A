# page_loans.py - collect every page of loans
import os
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:8000"
headers = {"X-API-Key": os.environ.get("NB_API_KEY",
                                       "northbridge-demo")}

all_loans = []
page = 1
while True:
    response = requests.get(f"{BASE_URL}/loans",
                            params={"page": page},
                            headers=headers, timeout=10)
    response.raise_for_status()
    body = response.json()
    all_loans.extend(body["loans"])
    print(f"page {body['page']}/{body['pages']}: "
          f"{len(body['loans'])} loans")
    if body["page"] == body["pages"]:
        break
    page += 1

loans = pd.DataFrame(all_loans)
print("Collected:", len(loans), "| API total:", body["total"])
assert len(loans) == body["total"] == 1200
assert loans["loan_id"].is_unique

Path("output").mkdir(exist_ok=True)
loans.to_csv("output/loans_from_api.csv", index=False)
print("Written output/loans_from_api.csv")
