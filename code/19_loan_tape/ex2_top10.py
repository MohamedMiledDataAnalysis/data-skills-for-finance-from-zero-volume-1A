"""ex2_top10.py - Exercise 2: the ten largest loans."""
from tapecheck import load_tape, RULES, clean_tape

raw, tape = load_tape()
clean, quarantine, log = clean_tape(tape, RULES)

top = clean.nlargest(10, "current_balance")
total = clean["current_balance"].sum()
top = top.assign(pct_pool=top["current_balance"] / total * 100)
cols = ["loan_id", "region", "current_balance",
        "current_ltv", "pct_pool"]
print(top[cols].to_string(index=False, float_format="{:,.2f}"
                          .format))
share = top["current_balance"].sum() / total * 100
print(f"Top 10 share of pool balance: {share:.2f}%")
print(f"Average loan share: {100 / len(clean):.3f}%")
