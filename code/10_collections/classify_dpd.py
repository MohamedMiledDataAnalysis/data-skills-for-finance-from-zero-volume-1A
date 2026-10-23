# classify_dpd.py - arrears bucket from days past due
days_past_due = 45

if days_past_due == 0:
    bucket = "Performing"
elif days_past_due < 30:
    bucket = "Early arrears"
elif days_past_due < 90:
    bucket = "30+ DPD"
else:
    bucket = "90+ DPD"

print(f"{days_past_due} days past due -> {bucket}")
