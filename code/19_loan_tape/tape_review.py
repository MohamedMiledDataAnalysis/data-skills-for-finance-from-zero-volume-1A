"""
tape_review.py - the investor pre-sale pack for a loan tape.

Run from the northbridge/ folder:
    python code/19_loan_tape/tape_review.py
"""

import pandas as pd

from tapecheck import (TAPE_FILE, CONTROL_FILE, CUTOFF, OUTPUT,
                       RULES, load_tape, profile, run_checks,
                       reconcile, clean_tape, pool_summary,
                       standard_strats, make_charts,
                       write_workbook, fmt)


def main():
    OUTPUT.mkdir(exist_ok=True)
    raw, tape = load_tape(TAPE_FILE)
    control = pd.read_csv(CONTROL_FILE)
    print(f"Tape {TAPE_FILE}: {len(tape)} rows, "
          f"cut-off {CUTOFF.date()}")

    summary, exceptions = run_checks(tape, RULES)
    failed = summary[summary["result"] == "Fail"]
    print(f"Rules failed: {len(failed)} of {len(summary)} "
          f"({(failed['severity'] == 'Critical').sum()} "
          f"Critical), {len(exceptions)} exceptions")

    recon = reconcile(tape, control)
    gaps = (recon["diff"] != 0).sum()
    print(f"Reconciliation: {gaps} of {len(recon)} measures "
          f"differ from the control file")

    clean, quarantine, log = clean_tape(tape, RULES)
    quarantine.to_csv(OUTPUT / "loan_tape_quarantine.csv",
                      index=False)
    print(f"Analysis set: {len(clean)} loans; "
          f"quarantined: {len(quarantine)} rows; "
          f"corrections: {(log['action'] == 'Corrected').sum()}")

    write_workbook(OUTPUT / "loan_tape_dq_report.xlsx", {
        "Summary": summary,
        "Exceptions": exceptions,
        "Reconciliation": recon.reset_index(names="measure"),
        "Corrections": log,
        "Profile": profile(tape).astype(str),
    })

    pool = pool_summary(clean)
    strats = standard_strats(clean)
    sheets = {"Pool": pool}
    sheets.update({k: t.round(2) for k, t in strats.items()})
    write_workbook(OUTPUT / "loan_tape_strats.xlsx", sheets)
    make_charts(strats)

    print()
    pool["value"] = pool["value"].map(fmt)
    print(pool.to_string(index=False))


if __name__ == "__main__":
    main()
