# compound_interest.py - interest earns interest
principal = 10000.00
annual_rate = 0.045
years = 3

# Annual compounding: one interest payment a year
annual = principal * (1 + annual_rate) ** years

# Monthly compounding: twelve smaller payments a year
monthly_rate = annual_rate / 12
months = years * 12
monthly = principal * (1 + monthly_rate) ** months

print(f"Annual compounding:  £{annual:,.2f}")
print(f"Monthly compounding: £{monthly:,.2f}")
print(f"Difference:          £{monthly - annual:,.2f}")

# Annual equivalent rate (AER) of the monthly product
aer = (1 + monthly_rate) ** 12 - 1
print(f"AER of 4.50% compounded monthly: {aer:.4%}")
