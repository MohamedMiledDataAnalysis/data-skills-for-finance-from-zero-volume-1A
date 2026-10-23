from monthly_report import (load_loans, load_customers,
                            load_fx, load_accounts, check_data)

loans = load_loans()
customers = load_customers()
fx = load_fx()
accounts = load_accounts()
check_data(loans, customers, accounts, fx)

bad = loans.copy()
bad.loc[0, "status"] = "Late"
check_data(bad, customers, accounts, fx)
