# ex1_to_gbp.py - Exercise 1: a currency conversion function
def to_gbp(amount, units_per_gbp, fee_pct=0.0):
    """Convert a foreign amount into pounds, less a fee.

    amount         amount in the foreign currency
    units_per_gbp  foreign units per £1 (EUR 1.1366 = €1.1366)
    fee_pct        conversion fee in per cent (default 0)
    """
    if units_per_gbp <= 0:
        raise ValueError(
            f"units_per_gbp must be > 0, got {units_per_gbp}"
        )
    gbp = amount / units_per_gbp
    return round(gbp * (1 - fee_pct / 100), 2)


print(to_gbp(3529.50, 1.1366))
print(to_gbp(12500.00, 1.1604, fee_pct=0.75))
try:
    to_gbp(100.00, 0)
except ValueError as error:
    print(f"Rejected: {error}")
