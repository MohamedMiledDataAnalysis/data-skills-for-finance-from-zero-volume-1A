# bom_demo.py - the byte order mark of Excel's CSV UTF-8
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv", nrows=3)
loans.to_csv("output/loans_for_excel.csv", index=False,
             encoding="utf-8-sig")

with open("output/loans_for_excel.csv", encoding="utf-8") as f:
    print(repr(f.readline()))

with open("output/loans_for_excel.csv", encoding="utf-8-sig") as f:
    print(repr(f.readline()))

check = pd.read_csv("output/loans_for_excel.csv",
                    encoding="utf-8")
print(repr(check.columns[0]))
