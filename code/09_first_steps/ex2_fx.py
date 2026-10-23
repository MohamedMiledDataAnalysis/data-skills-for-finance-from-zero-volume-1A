# ex2_fx.py - Exercise 2: USD payment converted to pounds
usd_amount = 12500.00
usd_per_gbp = 1.1604        # rate on 2025-12-31
fee_rate = 0.0075           # 0.75% conversion fee

gbp_before_fee = usd_amount / usd_per_gbp
fee = gbp_before_fee * fee_rate
gbp_credited = gbp_before_fee - fee

print(f"${usd_amount:,.2f} at {usd_per_gbp} "
      f"= £{gbp_before_fee:,.2f}")
print(f"Fee at {fee_rate:.2%}: £{fee:,.2f}")
print(f"Credited to account: £{gbp_credited:,.2f}")
