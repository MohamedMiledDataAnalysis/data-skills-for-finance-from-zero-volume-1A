# ex2_fx_dict.py - Exercise 2: convert balances with a rate table
rates_per_gbp = {"GBP": 1.0, "EUR": 1.1366, "USD": 1.1604}

balances = [("A00001", "GBP", 748.68),
            ("A00002", "EUR", 3529.50),
            ("A00009", "USD", 45906.31),
            ("A00120", "EUR", -137.14)]

total_gbp = 0.0
for account_id, currency, amount in balances:
    gbp = round(amount / rates_per_gbp[currency], 2)
    total_gbp = total_gbp + gbp
    print(f"{account_id} {currency} {amount:>10,.2f} "
          f"= £{gbp:>10,.2f}")
print(f"Total in pounds: £{total_gbp:,.2f}")
print(rates_per_gbp.get("CHF", "rate missing"))
