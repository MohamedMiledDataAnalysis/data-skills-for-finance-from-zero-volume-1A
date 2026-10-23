"""clean.py - build the analysis set and the corrections log."""
from tapecheck import load_tape, RULES, clean_tape, OUTPUT

raw, tape = load_tape()
clean, quarantine, log = clean_tape(tape, RULES)

print("Rows in tape:      ", len(tape))
print("Rows quarantined:  ", len(quarantine))
print("Rows for analysis: ", len(clean))
print(log["action"].value_counts().to_string())
fixes = log[log["action"] == "Corrected"]
print(fixes.drop(columns=["action", "reason"])
      .to_string(index=False))

OUTPUT.mkdir(exist_ok=True)
quarantine.to_csv(OUTPUT / "loan_tape_quarantine.csv",
                  index=False)
log.to_csv(OUTPUT / "loan_tape_corrections_log.csv",
           index=False)
print("Saved output/loan_tape_quarantine.csv")
