"""ex4_reused.py - Exercise 4: the two reused loan_ids."""
from tapecheck import load_tape

raw, tape = load_tape()
tape = tape.drop_duplicates()
reused = tape[tape["loan_id"].duplicated(keep=False)]
cols = ["loan_id", "borrower_id", "original_balance",
        "region"]
print(reused[cols].to_string())

same_borrower = tape[tape["borrower_id"].isin(
    reused["borrower_id"])]
print(same_borrower[cols].sort_values("borrower_id")
      .to_string())

others = tape.columns.drop(["loan_id", "origination_raw"])
copies = tape.duplicated(subset=others, keep=False)
print(tape.loc[copies & tape.index.isin(reused.index),
               ["loan_id", "borrower_id"]])
