# ex4_dates.py - Exercise 4: months on book with bad dates
from datetime import date

from nbfinance import months_between

reporting = date(2025, 12, 31)
loans = [("L00001", "2020-11-23"), ("L00007", "2025-09-07"),
         ("L09001", "2025-02-30"), ("L09002", "2026-03-01")]

for loan_id, text in loans:
    try:
        start = date.fromisoformat(text)
        mob = months_between(start, reporting)
        days = (reporting - start).days
        print(f"{loan_id}: {mob} months, {days} days on book")
    except ValueError as error:
        print(f"{loan_id}: skipped ({error})")
