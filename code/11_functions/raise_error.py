# raise_error.py - refusing invalid inputs
def monthly_rate(annual_rate_pct):
    """Convert a yearly rate in per cent to a monthly decimal."""
    if annual_rate_pct < 0 or annual_rate_pct > 100:
        raise ValueError(
            f"annual_rate_pct must be 0-100, got {annual_rate_pct}"
        )
    return annual_rate_pct / 100 / 12


print(monthly_rate(4.5))
try:
    monthly_rate(450)
except ValueError as error:
    print(f"Rejected: {error}")
monthly_rate(-1)
