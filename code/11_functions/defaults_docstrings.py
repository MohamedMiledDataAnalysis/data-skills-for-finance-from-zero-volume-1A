# defaults_docstrings.py - default arguments and docstrings
def compound(principal, annual_rate, years, periods_per_year=12):
    """Return the value of a deposit with compound interest.

    principal         amount deposited, in pounds
    annual_rate       yearly rate as a decimal (0.045 = 4.5%)
    years             number of years
    periods_per_year  compounding periods a year (default 12)
    """
    rate = annual_rate / periods_per_year
    periods = years * periods_per_year
    return principal * (1 + rate) ** periods


print(f"£{compound(10000, 0.045, 3):,.2f}")
print(f"£{compound(10000, 0.045, 3, 1):,.2f}")
print(f"£{compound(10000, 0.045, 3, periods_per_year=4):,.2f}")
print(compound.__doc__)
