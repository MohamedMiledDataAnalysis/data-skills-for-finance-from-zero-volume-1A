# ex1_lists.py - Exercise 1: interest rates of the first ten loans
rates = [7.81, 7.04, 6.62, 5.94, 7.88, 6.90, 3.60, 7.34, 7.14, 3.85]

print(f"Number of loans: {len(rates)}")
print(f"Lowest rate:     {min(rates):.2f}%")
print(f"Highest rate:    {max(rates):.2f}%")
print(f"Average rate:    {sum(rates) / len(rates):.2f}%")
print(f"Three highest:   {sorted(rates, reverse=True)[:3]}")
print(f"Above 7%:        {len([r for r in rates if r > 7])}")
