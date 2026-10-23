# lists.py - an ordered collection of values
balances = [748.68, 3529.50, -120.00, 15200.00, 410.25]

print(balances)
print(balances[0])          # first item
print(balances[-1])         # last item
print(balances[1:3])        # items 1 and 2
print(len(balances))        # number of items
print(sum(balances))        # total
print(min(balances), max(balances))
print(sorted(balances))
print(sorted(balances, reverse=True))

balances.append(980.00)     # add an item at the end
print(balances)
print(len(balances))
