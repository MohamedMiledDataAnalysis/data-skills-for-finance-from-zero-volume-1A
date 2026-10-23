# while_savings.py - months until a savings target is reached
balance = 2000.00          # starting balance
monthly_deposit = 350.00
annual_rate = 0.041
target = 15000.00

monthly_rate = annual_rate / 12
months = 0

while balance < target:
    balance = balance * (1 + monthly_rate) + monthly_deposit
    months = months + 1

years = months // 12
extra = months % 12
print(f"Target reached after {months} months "
      f"({years} years and {extra} months)")
print(f"Balance then: £{balance:,.2f}")
