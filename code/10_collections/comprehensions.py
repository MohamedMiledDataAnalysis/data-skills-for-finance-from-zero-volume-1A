# comprehensions.py - build a new list from an old one
balances = [748.68, 3529.50, -120.00, 15200.00, -45.10, 410.25]

overdrawn = [b for b in balances if b < 0]
print(overdrawn)

in_eur = [round(b * 1.1366, 2) for b in balances]
print(in_eur)

positive_total = sum([b for b in balances if b > 0])
print(f"£{positive_total:,.2f}")
