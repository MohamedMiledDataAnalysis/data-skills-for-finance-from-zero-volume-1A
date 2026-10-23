# ex2_buckets.py - Exercise 2: test dpd_bucket on boundaries
from nbfinance import dpd_bucket

for dpd in [0, 1, 29, 30, 89, 90, 365, -5]:
    try:
        print(f"{dpd:>4} -> {dpd_bucket(dpd)}")
    except ValueError as error:
        print(f"{dpd:>4} -> error: {error}")
