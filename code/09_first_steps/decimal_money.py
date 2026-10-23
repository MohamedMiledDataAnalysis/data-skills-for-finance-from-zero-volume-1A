# decimal_money.py - exact arithmetic for money
from decimal import Decimal, ROUND_HALF_UP

print(Decimal("0.1") + Decimal("0.2"))
print(Decimal(0.1))                  # a float carries its error

PENNY = Decimal("0.01")

balance = Decimal("1000.00")
rate = Decimal("0.0425")             # 4.25% a year
days = Decimal("31")

interest = balance * rate * days / Decimal("365")
print(interest)
print(interest.quantize(PENNY, rounding=ROUND_HALF_UP))

print(Decimal("2.675").quantize(PENNY, rounding=ROUND_HALF_UP))
print(round(2.675, 2))               # float rounding surprise
