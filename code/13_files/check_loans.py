# check_loans.py - data checks after a load
import pandas as pd

loans = pd.read_excel("data/excel/northbridge.xlsx",
                      sheet_name="loans",
                      dtype={"loan_id": "str"})

print("Rows:", len(loans))
print("Duplicate loan_id:", loans["loan_id"].duplicated().sum())
print("Missing values per column:")
print(loans.isna().sum())

mortgages = loans[loans["product"] == "Mortgage"]
print("Mortgages without LTV:", mortgages["ltv"].isna().sum())
print("Rate range:", loans["interest_rate"].min(),
      "to", loans["interest_rate"].max())
print("Principal <= 0:", (loans["principal"] <= 0).sum())
print("LTV outside 0-100:",
      (~loans["ltv"].dropna().between(0, 100)).sum())
