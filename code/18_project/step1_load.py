from monthly_report import (load_loans, load_customers,
                            load_fx, load_accounts)

loans = load_loans()
customers = load_customers()
fx = load_fx()
accounts = load_accounts()
print(accounts.head(3))
