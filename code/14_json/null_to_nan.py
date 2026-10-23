# null_to_nan.py - how null arrives in Python and pandas
import json

import pandas as pd

with open("data/json/loans.json", encoding="utf-8") as f:
    loans = json.load(f)
print("json module:", loans[0]["loan_id"], loans[0]["ltv"])

df = pd.read_json("data/json/loans.json")
print("pandas:     ", df.loc[0, "loan_id"], df.loc[0, "ltv"])
print("missing ltv:", df["ltv"].isna().sum())
