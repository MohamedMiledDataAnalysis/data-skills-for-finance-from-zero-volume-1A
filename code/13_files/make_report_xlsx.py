# make_report_xlsx.py - a workbook with a title above the table
from pathlib import Path

import pandas as pd

title_row = pd.DataFrame([["Northbridge Bank – Loan report"]])
data = pd.read_csv("data/csv/loans.csv", nrows=5)
Path("output").mkdir(exist_ok=True)
with pd.ExcelWriter("output/loan_report_raw.xlsx") as writer:
    title_row.to_excel(writer, sheet_name="Report",
                       index=False, header=False)
    data.to_excel(writer, sheet_name="Report",
                  index=False, startrow=2)
print("Written output/loan_report_raw.xlsx")
