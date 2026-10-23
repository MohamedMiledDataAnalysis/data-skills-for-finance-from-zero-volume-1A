# ex4_types.py - Exercise 4: text from a file into numbers
principal_text = "297735.46"
rate_text = "7.81"
term_text = "60"

principal = float(principal_text)
rate = float(rate_text) / 100       # 7.81 -> 0.0781
term = int(term_text)

first_year_interest = principal * rate
print(type(principal_text), type(principal))
print(f"Principal:  £{principal:,.2f}")
print(f"Rate:       {rate:.2%}")
print(f"Term:       {term} months ({term / 12:.1f} years)")
print(f"Year-one interest: £{first_year_interest:,.2f}")
