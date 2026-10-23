"""ex1_property.py - Exercise 1: strat by property type."""
from tapecheck import (load_tape, RULES, clean_tape, stratify,
                       show)

raw, tape = load_tape()
clean, quarantine, log = clean_tape(tape, RULES)
order = ["Detached", "Semi-detached", "Terraced", "Flat"]
print(show(stratify(clean, "property_type", labels=order)))
