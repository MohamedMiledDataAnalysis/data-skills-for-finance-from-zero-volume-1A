# savings_quote.py - Applied example: a fixed-rate saver quote
from decimal import Decimal, ROUND_HALF_UP

PENNY = Decimal("0.01")

customer = "Priya Thompson"
customer_id = "C0123"
deposit = Decimal("25000.00")       # pounds
annual_rate = Decimal("0.041")      # 4.10% a year
years = 2
eur_per_gbp = Decimal("1.1366")     # rate on 2025-12-31

monthly_rate = annual_rate / 12
months = years * 12
maturity = deposit * (1 + monthly_rate) ** months
maturity = maturity.quantize(PENNY, rounding=ROUND_HALF_UP)
interest = maturity - deposit
aer = (1 + monthly_rate) ** 12 - 1
maturity_eur = (maturity * eur_per_gbp).quantize(
    PENNY, rounding=ROUND_HALF_UP
)

print("Northbridge Bank - 2-Year Fixed Saver quote")
print("-" * 44)
print(f"Customer:        {customer} ({customer_id})")
print(f"Deposit:         £{deposit:,.2f}")
print(f"Gross rate:      {annual_rate:.2%} p.a., monthly")
print(f"AER:             {aer:.2%}")
print(f"Term:            {months} months")
print(f"Interest earned: £{interest:,.2f}")
print(f"Maturity value:  £{maturity:,.2f}")
print(f"In euros:        €{maturity_eur:,.2f} at {eur_per_gbp}")
