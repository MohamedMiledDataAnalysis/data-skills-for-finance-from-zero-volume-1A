# read_excel_skiprows.py - skip the title rows of a sheet
import pandas as pd

raw = pd.read_excel("output/loan_report_raw.xlsx", header=None)
print(raw.iloc[:4, :4])

report = pd.read_excel("output/loan_report_raw.xlsx",
                       skiprows=2)
print(report.iloc[:, :5])
