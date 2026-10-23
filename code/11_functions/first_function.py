# first_function.py - define a function and call it
def simple_interest(principal, annual_rate, years):
    interest = principal * annual_rate * years
    return interest


a = simple_interest(10000, 0.045, 3)
b = simple_interest(2500, 0.0425, 1)
print(f"£{a:,.2f}")
print(f"£{b:,.2f}")
print(f"£{a + b:,.2f}")
