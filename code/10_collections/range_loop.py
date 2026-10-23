# range_loop.py - a year-by-year balance table
balance = 10000.00
annual_rate = 0.045

print(list(range(5)))
print(list(range(1, 6)))

for year in range(1, 6):
    balance = balance * (1 + annual_rate)
    print(f"Year {year}: £{balance:,.2f}")
