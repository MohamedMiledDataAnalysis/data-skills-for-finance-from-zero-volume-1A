# ex4_card_payoff.py - Exercise 4: months to clear a card balance
balance = 5000.00
monthly_rate = 0.015       # 1.5% a month
payment = 200.00

months = 0
total_interest = 0.0
while balance > 0:
    interest = balance * monthly_rate
    total_interest = total_interest + interest
    balance = balance + interest - payment
    months = months + 1

print(f"Cleared after {months} months")
print(f"Total interest paid: £{total_interest:,.2f}")
print(f"Last month's overpayment: £{-balance:,.2f}")
