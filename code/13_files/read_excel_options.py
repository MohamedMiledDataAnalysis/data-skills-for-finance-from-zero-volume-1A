# read_excel_options.py - usecols, engine and skiprows in Excel
import pandas as pd

fx = pd.read_excel(
    "data/excel/northbridge.xlsx",
    sheet_name="fx_rates",
    usecols="A:C",
    engine="openpyxl",
)
print(fx.head(4))
print(fx.dtypes)

loans = pd.read_excel(
    "data/excel/northbridge.xlsx",
    sheet_name="loans",
    usecols=["loan_id", "product", "principal"],
    skiprows=range(1, 1001),
)
print(loans.head(3))
print(len(loans), "rows")
