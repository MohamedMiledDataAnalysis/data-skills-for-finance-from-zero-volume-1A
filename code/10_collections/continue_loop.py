# continue_loop.py - skip items with continue
balances = [748.68, 0.00, -120.00, 0.00, 410.25]

for balance in balances:
    if balance == 0:
        continue          # dormant account: nothing to report
    print(f"£{balance:,.2f}")
