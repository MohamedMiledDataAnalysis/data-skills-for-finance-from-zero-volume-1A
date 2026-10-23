# dayfirst_demo.py - what happens without dayfirst=True
import io

import pandas as pd

files = {
    "ambiguous first": "d\n01/07/2020\n02/03/2021\n",
    "ambiguous, then 31/12": "d\n01/07/2020\n31/12/2021\n",
    "with dayfirst=True": "d\n01/07/2020\n02/03/2021\n",
}
for label, text in files.items():
    first = label == "with dayfirst=True"
    df = pd.read_csv(io.StringIO(text), parse_dates=["d"],
                     dayfirst=first)
    print(f"{label:<22}{str(df['d'].dtype):<15}",
          df["d"].astype(str).tolist())
