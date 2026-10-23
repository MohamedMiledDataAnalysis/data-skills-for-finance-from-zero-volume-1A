# ex2_loans_json_checks.py - Exercise 2, checks on loans.json
import pandas as pd

loans = pd.read_json("data/json/loans.json",
                     dtype={"loan_id": "str"})
loans["origination_date"] = pd.to_datetime(
    loans["origination_date"])

print("Rows:", len(loans))
print("Duplicate loan_id:", loans["loan_id"].duplicated().sum())
print("Missing ltv:", loans["ltv"].isna().sum())
print("Non-mortgages:", (loans["product"] != "Mortgage").sum())
print("Earliest:", loans["origination_date"].min().date())
print("Latest:", loans["origination_date"].max().date())
