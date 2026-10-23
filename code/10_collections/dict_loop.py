# dict_loop.py - loop over a dictionary
exposure = {"Mortgage": 1250000.0, "Personal": 84000.0,
            "Auto": 61500.0, "SME": 930000.0}

for product, amount in exposure.items():
    print(f"{product:<10} {amount:>14,.2f}")

total = sum(exposure.values())
print(f"{'Total':<10} {total:>14,.2f}")
