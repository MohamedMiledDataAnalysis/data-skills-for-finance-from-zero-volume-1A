# stdlib_modules.py - math and datetime
import math
from datetime import date

print(math.sqrt(250000))
print(math.floor(7.99), math.ceil(7.01))
print(math.log(2) / math.log(1.045))   # years to double at 4.5%

origination = date.fromisoformat("2020-11-23")   # loan L00001
reporting = date(2025, 12, 31)
print(origination, reporting)
print(origination.year, origination.month, origination.day)

days = (reporting - origination).days
print(f"Days on book: {days}")

months_on_book = ((reporting.year - origination.year) * 12
                  + reporting.month - origination.month)
if reporting.day < origination.day:
    months_on_book -= 1
print(f"Months on book: {months_on_book}")
print(f"Reporting date: {reporting:%d %B %Y}")
