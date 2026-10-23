# page_types.py - check the types an API sends
import pandas as pd
import requests

response = requests.get(
    "http://127.0.0.1:8000/loans",
    params={"page": 1},
    headers={"X-API-Key": "northbridge-demo"},
    timeout=10,
)
first = response.json()["loans"][0]
print(first)

loans = pd.DataFrame(response.json()["loans"])
print(loans.dtypes.value_counts())

numeric = ["principal", "interest_rate", "term_months", "ltv"]
loans[numeric] = loans[numeric].apply(pd.to_numeric)
print(loans[numeric].dtypes)
print(f"Page 1 principal: £{loans['principal'].sum():,.2f}")
