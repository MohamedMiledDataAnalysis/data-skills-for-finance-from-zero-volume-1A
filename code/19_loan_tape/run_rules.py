"""run_rules.py - run the rule catalogue, write the DQ report."""
from tapecheck import (load_tape, RULES, run_checks,
                       write_workbook)

raw, tape = load_tape()
summary, exceptions = run_checks(tape, RULES)
print(summary[["rule_id", "dimension", "severity",
               "failed_rows", "result"]].to_string(index=False))
print("Exception rows:", len(exceptions))
print(exceptions.head(4).to_string(index=False))
write_workbook("output/loan_tape_dq_report.xlsx",
               {"Summary": summary, "Exceptions": exceptions})
