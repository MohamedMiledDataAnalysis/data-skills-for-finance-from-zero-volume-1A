# book_balances.py - Applied example: instalments and balances
import csv
from datetime import date

from nbfinance import amortisation, monthly_payment, months_between

REPORTING_DATE = date(2025, 12, 31)

instalments = {}    # total monthly instalment per product
balances = {}       # total outstanding balance per product
rejected = []       # loans that could not be calculated

with open("data/csv/loans.csv", newline="") as f:
    for row in csv.DictReader(f):
        try:
            principal = float(row["principal"])
            rate = float(row["interest_rate"])
            term = int(row["term_months"])
            start = date.fromisoformat(row["origination_date"])
            payment = monthly_payment(principal, rate, term)
        except ValueError as error:
            rejected.append((row["loan_id"], str(error)))
            continue
        mob = months_between(start, REPORTING_DATE)
        if mob == 0:
            balance = principal
        elif mob >= term:
            balance = 0.0
        else:
            balance = amortisation(principal, rate, term)[mob - 1][
                "closing"
            ]
        product = row["product"]
        if balance > 0:                 # live loans only
            instalments[product] = (
                instalments.get(product, 0) + payment
            )
        balances[product] = balances.get(product, 0) + balance

print(f"Northbridge loan book at {REPORTING_DATE:%d %B %Y}")
print(f"{'Product':<10}{'Monthly instalments':>21}"
      f"{'Outstanding':>18}")
for product in sorted(balances, key=balances.get, reverse=True):
    print(f"{product:<10}{instalments[product]:>21,.2f}"
          f"{balances[product]:>18,.2f}")
print(f"{'Total':<10}{sum(instalments.values()):>21,.2f}"
      f"{sum(balances.values()):>18,.2f}")
print(f"Rejected rows: {len(rejected)}")
