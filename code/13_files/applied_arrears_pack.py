# applied_arrears_pack.py - monthly arrears pack from Excel
from pathlib import Path

import pandas as pd

pd.options.display.float_format = "{:,.2f}".format

# 1. Extract: the loan book from the Excel workbook
loans = pd.read_excel(
    "data/excel/northbridge.xlsx",
    sheet_name="loans",
    dtype={"loan_id": "str", "customer_id": "str"},
    parse_dates=["origination_date"],
)

# 2. Check: the load is complete and clean
checks = pd.DataFrame({
    "check": ["rows loaded", "duplicate loan_id",
              "missing principal", "rate outside 0-20%"],
    "value": [len(loans),
              loans["loan_id"].duplicated().sum(),
              loans["principal"].isna().sum(),
              (~loans["interest_rate"].between(0, 20)).sum()],
    "expected": [1200, 0, 0, 0],
})
checks["passed"] = checks["value"] == checks["expected"]
print(checks)
if not checks["passed"].all():
    raise SystemExit("Load checks failed: report not written")

# 3. Analyse: loans not performing, by product and status
arrears = loans[loans["status"] != "Performing"]
summary = (arrears.groupby(["product", "status"])
           .agg(loans=("loan_id", "count"),
                principal=("principal", "sum"))
           .reset_index())
share = arrears["principal"].sum() / loans["principal"].sum()
print(summary)
print(f"Arrears share of book: {share:.2%}")

# 4. Load: one workbook, three sheets
Path("output").mkdir(exist_ok=True)
with pd.ExcelWriter("output/arrears_pack.xlsx") as writer:
    summary.to_excel(writer, sheet_name="summary", index=False)
    arrears.to_excel(writer, sheet_name="arrears_list",
                     index=False)
    checks.to_excel(writer, sheet_name="load_checks",
                    index=False)
print("Written output/arrears_pack.xlsx")
