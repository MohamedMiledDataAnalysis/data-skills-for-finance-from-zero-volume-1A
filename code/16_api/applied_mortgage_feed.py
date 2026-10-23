# applied_mortgage_feed.py - mortgage arrears by LTV band
import os
from pathlib import Path

import pandas as pd

from retry import get_with_retry

pd.options.display.float_format = "{:,.2f}".format
BASE_URL = "http://127.0.0.1:8000"
api_key = os.environ.get("NB_API_KEY")
if api_key is None:
    raise SystemExit("Set NB_API_KEY first.")
headers = {"X-API-Key": api_key}

# 1. Extract: every page of mortgages
rows, page = [], 1
while True:
    body = get_with_retry(f"{BASE_URL}/loans",
                          params={"product": "Mortgage",
                                  "page": page},
                          headers=headers).json()
    rows.extend(body["loans"])
    if body["page"] == body["pages"]:
        break
    page += 1
mortgages = pd.DataFrame(rows)

# 2. Check: complete, unique, only mortgages
assert len(mortgages) == body["total"]
assert mortgages["loan_id"].is_unique
assert (mortgages["product"] == "Mortgage").all()
print(f"{len(mortgages)} mortgages from {body['pages']} pages")

# 3. Fix types: the API sends every value as text
numeric = ["principal", "interest_rate", "term_months", "ltv"]
mortgages[numeric] = mortgages[numeric].apply(pd.to_numeric)

# 4. Analyse: arrears by loan-to-value band
mortgages["ltv_band"] = pd.cut(
    mortgages["ltv"], bins=[0, 60, 80, 90, 100],
    labels=["<=60%", "60-80%", "80-90%", ">90%"])
in_arrears = mortgages["status"] != "Performing"
mortgages["arrears_principal"] = (mortgages["principal"]
                                  .where(in_arrears, 0))
bands = (mortgages.groupby("ltv_band", observed=True)
         .agg(loans=("loan_id", "count"),
              principal=("principal", "sum"),
              arrears=("arrears_principal", "sum")))
bands["arrears_rate_pct"] = (100 * bands["arrears"]
                             / bands["principal"]).round(2)
print(bands)

# 5. Load: save for the risk team
Path("output").mkdir(exist_ok=True)
mortgages.to_csv("output/mortgages_from_api.csv", index=False)
bands.to_csv("output/mortgage_ltv_bands.csv")
print("Written output/mortgages_from_api.csv and "
      "output/mortgage_ltv_bands.csv")
