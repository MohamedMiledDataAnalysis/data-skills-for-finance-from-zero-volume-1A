"""pool.py - the pool summary a rating agency asks for."""
from tapecheck import (load_tape, RULES, clean_tape,
                       pool_summary, fmt)

raw, tape = load_tape()
clean, quarantine, log = clean_tape(tape, RULES)
pool = pool_summary(clean)
pool["value"] = pool["value"].map(fmt)
print(pool.to_string(index=False))
