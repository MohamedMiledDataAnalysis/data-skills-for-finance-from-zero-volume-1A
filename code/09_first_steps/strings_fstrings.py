# strings_fstrings.py - text and formatted output
first_name = "Olivia"
last_name = "Smith"
full_name = first_name + " " + last_name
print(full_name)
print(full_name.upper())
print(len(full_name))

balance = 1234567.891
rate = 0.0425
print(f"Customer: {full_name}")
print(f"Balance: £{balance:,.2f}")
print(f"Rate: {rate:.2%}")
print(f"Loan ID: L{42:05d}")
