# for_loops.py - repeat an action for each item
dpd_values = [0, 12, 30, 89, 90, 240]

for dpd in dpd_values:
    if dpd == 0:
        bucket = "Performing"
    elif dpd < 30:
        bucket = "Early arrears"
    elif dpd < 90:
        bucket = "30+ DPD"
    else:
        bucket = "90+ DPD"
    print(f"{dpd:>4} days -> {bucket}")

print("Done")
