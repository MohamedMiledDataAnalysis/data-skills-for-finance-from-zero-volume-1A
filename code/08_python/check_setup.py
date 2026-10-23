# check_setup.py - verify the Python workstation end to end
import sys

import matplotlib
import openpyxl
import pandas as pd
import plotly
import requests
import sqlalchemy

print("Python    ", sys.version.split()[0])
print("pandas    ", pd.__version__)
print("openpyxl  ", openpyxl.__version__)
print("requests  ", requests.__version__)
print("sqlalchemy", sqlalchemy.__version__)
print("matplotlib", matplotlib.__version__)
print("plotly    ", plotly.__version__)

loans = pd.read_csv("data/csv/loans.csv")
arrears = loans[loans["status"] != "Performing"]
print(f"Loans: {len(loans):,}  in arrears or default: "
      f"{len(arrears):,}")
print(f"Principal in arrears: £{arrears['principal'].sum():,.2f}")

health = requests.get("http://127.0.0.1:8000/health", timeout=10)
print("API health:", health.json())
