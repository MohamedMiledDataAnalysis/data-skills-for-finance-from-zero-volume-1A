# write_excel_sheets.py - a workbook with several sheets
import pandas as pd

pd.options.display.float_format = "{:,.2f}".format

loans = pd.read_csv("data/csv/loans.csv")

by_product = (loans.groupby("product")
              .agg(loans=("loan_id", "count"),
                   principal=("principal", "sum"))
              .reset_index())
arrears = loans[loans["status"] != "Performing"]

with pd.ExcelWriter("output/loan_summary.xlsx",
                    engine="openpyxl") as writer:
    by_product.to_excel(writer, sheet_name="by_product",
                        index=False)
    arrears.to_excel(writer, sheet_name="arrears", index=False)

check = pd.read_excel("output/loan_summary.xlsx", sheet_name=None)
for name, sheet in check.items():
    print(name, sheet.shape)
print(by_product)
