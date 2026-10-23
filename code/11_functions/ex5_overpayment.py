# ex5_overpayment.py - Exercise 5: effect of a monthly overpayment
from nbfinance import monthly_payment


def payoff(principal, annual_rate_pct, term_months, extra=0.0):
    """Return (months, total interest) with an overpayment."""
    if extra < 0:
        raise ValueError(f"extra must be >= 0, got {extra}")
    payment = round(
        monthly_payment(principal, annual_rate_pct, term_months), 2
    )
    r = annual_rate_pct / 100 / 12
    balance = principal
    months = 0
    total_interest = 0.0
    while balance > 0:
        interest = round(balance * r, 2)
        repaid = min(payment + extra - interest, balance)
        if months == term_months - 1:     # final payment
            repaid = balance
        balance = round(balance - repaid, 2)
        total_interest += interest
        months += 1
    return months, round(total_interest, 2)


base = payoff(250000, 4.5, 300)
over = payoff(250000, 4.5, 300, extra=200)
print(f"No overpayment: {base[0]} months, "
      f"£{base[1]:,.2f} interest")
print(f"£200 a month:   {over[0]} months, "
      f"£{over[1]:,.2f} interest")
saved = base[0] - over[0]
print(f"Saved: {saved} months and "
      f"£{base[1] - over[1]:,.2f} of interest")
