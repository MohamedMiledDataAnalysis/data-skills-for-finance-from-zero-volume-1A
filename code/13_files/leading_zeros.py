# leading_zeros.py - keep identifiers as text
from pathlib import Path

import pandas as pd

Path("output").mkdir(exist_ok=True)
Path("output/branches.csv").write_text(
    "sort_code,branch\n040004,London Wall\n"
    "090128,Leeds Briggate\n",
    encoding="utf-8",
)

as_numbers = pd.read_csv("output/branches.csv")
print(as_numbers)

as_text = pd.read_csv("output/branches.csv",
                      dtype={"sort_code": "str"})
print(as_text)
