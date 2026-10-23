"""reconcile.py - tape totals against the control totals."""
import pandas as pd

from tapecheck import load_tape, reconcile, CONTROL_FILE

raw, tape = load_tape()
control = pd.read_csv(CONTROL_FILE)
table = reconcile(tape, control)
print(table.to_string(float_format="{:,.0f}".format))
