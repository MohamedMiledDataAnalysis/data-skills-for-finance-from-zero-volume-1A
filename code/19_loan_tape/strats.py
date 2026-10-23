"""strats.py - stratification tables on the clean tape."""
from tapecheck import (load_tape, RULES, clean_tape,
                       standard_strats, show, write_workbook)

raw, tape = load_tape()
clean, quarantine, log = clean_tape(tape, RULES)
strats = standard_strats(clean)
for name, table in strats.items():
    print(f"--- {name}")
    print(show(table))

write_workbook("output/loan_tape_strats.xlsx",
               {name: t.round(2) for name, t in strats.items()})
