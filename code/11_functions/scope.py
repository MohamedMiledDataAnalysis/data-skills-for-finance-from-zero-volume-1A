# scope.py - variables inside a function stay inside
fee = 25.00


def apply_fee(balance):
    new_balance = balance - fee
    return new_balance


print(apply_fee(1000.00))
print(new_balance)
