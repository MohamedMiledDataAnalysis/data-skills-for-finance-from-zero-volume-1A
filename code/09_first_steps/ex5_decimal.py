# ex5_decimal.py - Exercise 5: daily interest with Decimal
from decimal import Decimal, ROUND_HALF_UP

PENNY = Decimal("0.01")
overdraft = Decimal("1847.35")      # amount overdrawn
rate = Decimal("0.199")             # 19.9% a year
days = 17

as_float = 1847.35 * 0.199 * 17 / 365
exact = overdraft * rate * days / 365
charge = exact.quantize(PENNY, rounding=ROUND_HALF_UP)

print(f"Float result:   {as_float}")
print(f"Decimal result: {exact}")
print(f"Charge posted:  £{charge}")
