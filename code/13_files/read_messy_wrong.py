# read_messy_wrong.py - three wrong ways to read a messy file
import pandas as pd

path = "output/loans_eu.csv"

# Attempt 1: no options at all
try:
    pd.read_csv(path)
except UnicodeDecodeError as error:
    print("Attempt 1 -> UnicodeDecodeError:", error)

# Attempt 2: right encoding, but the title row is still there
try:
    pd.read_csv(path, encoding="cp1252")
except pd.errors.ParserError as error:
    print("Attempt 2 -> ParserError:", error)

# Attempt 3: title row skipped, but separator still a comma
wrong = pd.read_csv(path, encoding="cp1252", skiprows=1)
print("Attempt 3 -> shape:", wrong.shape)
print(wrong.columns.tolist())
