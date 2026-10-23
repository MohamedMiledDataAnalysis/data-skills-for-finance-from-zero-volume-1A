# errors.py - catching errors with try and except
values = ["4.5", "4,5", ""]

for text in values:
    try:
        rate = float(text)
        print(f"{text!r} -> {rate}")
    except ValueError:
        print(f"{text!r} is not a number")

loans, defaults = 0, 0
try:
    default_rate = defaults / loans
except ZeroDivisionError:
    default_rate = None
print(f"Default rate: {default_rate}")

try:
    with open("data/csv/loans_2026.csv", newline="") as f:
        print(f.readline())
except FileNotFoundError as error:
    print(f"Cannot read the file: {error}")
