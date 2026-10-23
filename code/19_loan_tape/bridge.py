"""bridge.py - explain the current-balance difference."""
import pandas as pd

from tapecheck import load_tape, CONTROL_FILE


def scheduled_balance(t):
    r = t["interest_rate"] / 1200
    n = t["original_term_months"]
    k = t["seasoning_months"]
    p = t["original_balance"]
    payment = p * r / (1 - (1 + r) ** -n)
    growth = (1 + r) ** k
    return p * growth - payment * (growth - 1) / r


raw, tape = load_tape()
control = pd.read_csv(CONTROL_FILE)
tape = tape.drop_duplicates()

same = tape.drop(columns="loan_id").duplicated(keep=False)
reused = tape["loan_id"].duplicated(keep=False) & same
negative = tape["current_balance"] < 0
above = tape["current_balance"] > tape["original_balance"]

bal = tape["current_balance"]
excess = bal[above] - scheduled_balance(tape[above])
gap = bal.sum() - control.loc[0, "total_current_balance"]
items = pd.Series({
    "Reused loan_id rows (extra copies)": bal[reused].sum(),
    "Negative balances (sign flipped)": 2 * bal[negative].sum(),
    "Balances above schedule (DQ15)": excess.sum(),
})
items["Unexplained difference"] = gap - items.sum()
items["Total difference"] = gap
print(items.round(2).to_string())
