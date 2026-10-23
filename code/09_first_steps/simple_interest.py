# simple_interest.py - interest on the original amount only
principal = 10000.00      # amount deposited, in pounds
annual_rate = 0.045       # 4.5% a year, written as a decimal
years = 3

interest = principal * annual_rate * years
final_amount = principal + interest

print(f"Interest earned: £{interest:,.2f}")
print(f"Final amount:    £{final_amount:,.2f}")
