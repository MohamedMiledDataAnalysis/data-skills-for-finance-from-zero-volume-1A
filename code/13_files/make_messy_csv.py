# make_messy_csv.py - write a European-format CSV file
from pathlib import Path

import pandas as pd

loans = pd.read_csv("data/csv/loans.csv", nrows=6)
loans = loans[["loan_id", "product", "principal",
               "interest_rate", "origination_date"]]

lines = ["Northbridge Bank – Prêts en cours au 31/12/2025"]
lines.append(";".join(loans.columns))
for row in loans.itertuples(index=False):
    principal = f"{row.principal:,.2f}"
    principal = (principal.replace(",", " ")
                 .replace(".", ",").replace(" ", "."))
    rate = f"{row.interest_rate:.2f}".replace(".", ",")
    day = pd.Timestamp(row.origination_date)
    lines.append(";".join([row.loan_id, row.product, principal,
                           rate, day.strftime("%d/%m/%Y")]))

Path("output").mkdir(exist_ok=True)
path = Path("output/loans_eu.csv")
path.write_text("\n".join(lines) + "\n", encoding="cp1252")
print(path.read_text(encoding="cp1252"))
