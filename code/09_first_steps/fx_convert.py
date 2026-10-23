# fx_convert.py - convert pounds to euros and back
gbp_amount = 2500.00
eur_per_gbp = 1.1467      # Northbridge rate on 2025-03-31

eur_amount = gbp_amount * eur_per_gbp
print(f"£{gbp_amount:,.2f} = €{eur_amount:,.2f}")

eur_invoice = 8750.00
gbp_cost = eur_invoice / eur_per_gbp
print(f"€{eur_invoice:,.2f} = £{gbp_cost:,.2f}")
