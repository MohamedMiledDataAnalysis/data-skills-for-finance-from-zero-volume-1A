"""ex3_income.py - Exercise 3: income and loan-to-income rules."""
from tapecheck import load_tape, RULES, run_checks

raw, tape = load_tape()
lti = tape["original_balance"] / tape["borrower_income"]
print(lti.groupby(tape["occupancy"]).agg(["min", "max"])
      .round(2))

new_rules = RULES + [
    {"rule_id": "DQ19", "dimension": "Completeness",
     "severity": "Warning", "fields": ["borrower_income"],
     "description": "borrower_income blank or <= 0",
     "test": lambda t: ~(t["borrower_income"] > 0)},
    {"rule_id": "DQ20", "dimension": "Consistency",
     "severity": "Warning",
     "fields": ["original_balance", "borrower_income"],
     "description": "loan-to-income above 7",
     "test": lambda t: t["original_balance"]
                       / t["borrower_income"] > 7},
]

test = tape.copy()
test.loc[0, "borrower_income"] = 77.9
test.loc[1, "borrower_income"] = 0
for name, data in [("Real tape", tape), ("Test copy", test)]:
    summary, exceptions = run_checks(data, new_rules)
    print(name)
    print(summary.tail(2)[["rule_id", "failed_rows"]]
          .to_string(index=False))
print(exceptions.tail(3)[["loan_id", "rule_id", "values"]]
      .to_string(index=False))
