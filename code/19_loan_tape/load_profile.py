"""load_profile.py - read the tape as text, convert, profile."""
import pandas as pd

from tapecheck import load_tape, profile

raw, tape = load_tape()
print("Shape:", raw.shape)
print(raw.loc[:2, ["loan_id", "origination_date",
                   "interest_rate", "property_value"]])

bad = tape["origination_date"].isna()
print("Dates not in YYYY-MM-DD:", bad.sum())
print(tape.loc[bad, ["loan_id", "origination_raw"]])

pd.options.display.float_format = "{:,.0f}".format
prof = profile(tape)
print(prof.drop(columns="dtype").to_string(index=False))

for col in ["status", "repayment_type", "occupancy"]:
    print(col, tape[col].nunique(), "values:")
    print("  ", ", ".join(sorted(tape[col].unique())))
