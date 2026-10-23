"""charts.py - three charts of the clean pool."""
from tapecheck import (load_tape, RULES, clean_tape,
                       standard_strats, make_charts)

raw, tape = load_tape()
clean, quarantine, log = clean_tape(tape, RULES)
make_charts(standard_strats(clean))
