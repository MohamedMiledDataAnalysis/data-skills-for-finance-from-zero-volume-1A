# ex4_sme_pages.py - Exercise 4, a paging function
import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:8000"
headers = {"X-API-Key": "northbridge-demo"}


def fetch_all_loans(product):
    """Return every loan of one product, page by page."""
    rows, page = [], 1
    while True:
        response = requests.get(
            f"{BASE_URL}/loans",
            params={"product": product, "page": page},
            headers=headers, timeout=10)
        response.raise_for_status()
        body = response.json()
        rows.extend(body["loans"])
        if body["page"] == body["pages"]:
            return pd.DataFrame(rows), body["total"]
        page += 1


sme, total = fetch_all_loans("SME")
csv = pd.read_csv("data/csv/loans.csv")
expected = (csv["product"] == "SME").sum()
print("From API:", len(sme), "| API total:", total,
      "| loans.csv:", expected)
assert len(sme) == total == expected
sme["principal"] = pd.to_numeric(sme["principal"])
print(sme.groupby("status")["principal"].sum().round(2))
