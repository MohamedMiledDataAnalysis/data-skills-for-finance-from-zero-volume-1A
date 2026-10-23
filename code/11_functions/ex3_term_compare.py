# ex3_term_compare.py - Exercise 3: 30-, 25- and 20-year terms
from nbfinance import amortisation, monthly_payment

principal = 240497.34      # loan L00007
rate_pct = 3.6

for years in [30, 25, 20]:
    term = years * 12
    payment = monthly_payment(principal, rate_pct, term)
    schedule = amortisation(principal, rate_pct, term)
    interest = sum(row["interest"] for row in schedule)
    print(f"{years} years: £{payment:,.2f} a month, "
          f"total interest £{interest:,.2f}")
