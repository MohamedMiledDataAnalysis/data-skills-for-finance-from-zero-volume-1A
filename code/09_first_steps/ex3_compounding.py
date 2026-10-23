# ex3_compounding.py - Exercise 3: compounding frequency
principal = 50000.00
annual_rate = 0.05
years = 10

annual = principal * (1 + annual_rate) ** years
quarterly = principal * (1 + annual_rate / 4) ** (years * 4)
monthly = principal * (1 + annual_rate / 12) ** (years * 12)
daily = principal * (1 + annual_rate / 365) ** (years * 365)

print(f"Annual:    £{annual:,.2f}")
print(f"Quarterly: £{quarterly:,.2f}")
print(f"Monthly:   £{monthly:,.2f}")
print(f"Daily:     £{daily:,.2f}")
