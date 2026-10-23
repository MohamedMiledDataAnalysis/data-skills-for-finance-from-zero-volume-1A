# mortgage_schedule.py - use the nbfinance module
from nbfinance import amortisation, monthly_payment

principal = 250000.00
rate_pct = 4.5
term = 25 * 12

payment = monthly_payment(principal, rate_pct, term)
schedule = amortisation(principal, rate_pct, term)

print(f"Monthly payment: £{payment:,.2f}")
print(f"{'Period':>6} {'Opening':>12} {'Interest':>9} "
      f"{'Principal':>10} {'Closing':>12}")
for row in schedule[:3] + schedule[-1:]:
    print(f"{row['period']:>6} {row['opening']:>12,.2f} "
          f"{row['interest']:>9,.2f} {row['principal']:>10,.2f} "
          f"{row['closing']:>12,.2f}")

total_interest = sum(row["interest"] for row in schedule)
total_paid = total_interest + principal
print(f"Total interest paid: £{total_interest:,.2f}")
print(f"Total repaid:        £{total_paid:,.2f}")
print(f"Final closing balance: {schedule[-1]['closing']:.2f}")
