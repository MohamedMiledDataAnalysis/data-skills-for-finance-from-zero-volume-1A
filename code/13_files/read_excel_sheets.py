# read_excel_sheets.py - one sheet, several sheets, all sheets
import pandas as pd

path = "data/excel/northbridge.xlsx"

loans = pd.read_excel(path, sheet_name="loans")
print("One sheet:", type(loans).__name__, loans.shape)

pair = pd.read_excel(path, sheet_name=["customers", "accounts"])
print("List of sheets:", type(pair).__name__, list(pair))

book = pd.read_excel(path, sheet_name=None)
for name, sheet in book.items():
    print(f"{name:<20}{len(sheet):>6} rows")
