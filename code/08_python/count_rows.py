# count_rows.py - count the rows in every Northbridge CSV file
from pathlib import Path

import pandas as pd

for path in sorted(Path("data/csv").glob("*.csv")):
    table = pd.read_csv(path)
    print(f"{path.name:<20}{len(table):>7,} rows")
