"""ex5_month_on_month.py - Exercise 5: compare two tapes."""
import pandas as pd

from tapecheck import load_tape, RULES, clean_tape


def simulate_january(dec):
    jan = dec.copy()
    monthly_rate = jan["interest_rate"].fillna(0) / 1200
    jan["current_balance"] = (
        jan["current_balance"] * (1 + monthly_rate)
        - jan["monthly_payment"]).clip(lower=0).round(2)
    redeemed = jan.sample(4, random_state=2026).index
    jan = jan.drop(index=redeemed)
    capitalised = jan.sample(3, random_state=7).index
    jan.loc[capitalised, "current_balance"] += (
        2 * jan.loc[capitalised, "monthly_payment"])
    return jan


def compare(old, new, tolerance=1.0):
    both = old[["loan_id", "current_balance"]].merge(
        new[["loan_id", "current_balance"]], on="loan_id",
        how="outer", suffixes=("_old", "_new"),
        indicator=True)
    both = both.rename(columns={"current_balance_old": "old",
                                "current_balance_new": "new"})
    both["change"] = (both["new"] - both["old"]).round(2)
    both["flag"] = "OK"
    both.loc[both["_merge"] == "left_only", "flag"] = (
        "Disappeared")
    both.loc[both["_merge"] == "right_only", "flag"] = "New"
    both.loc[both["change"] > tolerance, "flag"] = "Balance up"
    return both.drop(columns="_merge")


raw, tape = load_tape()
dec, quarantine, log = clean_tape(tape, RULES)
jan = simulate_january(dec)
result = compare(dec, jan)
print(result["flag"].value_counts().to_string())
flagged = result[result["flag"] != "OK"]
print(flagged.to_string(index=False))
